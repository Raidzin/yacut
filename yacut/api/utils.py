from random import choice
from string import ascii_letters, digits

from yacut import db
from yacut.api.exceptions import ValidationError
from yacut.models import URLMap
from yacut.api.validators import validate_urls

URL = 'url'
SHORT_LINK = 'short_link'
CUSTOM_URL = 'custom_id'
BASE_URL = 'http://localhost/'


def _save_urls(original, short):
    url_map = URLMap(
        original=original,
        short=short,
    )
    db.session.add(url_map)
    db.session.commit()


def _get_random_url(original_url):
    try:
        return URLMap.query.filter(
            URLMap.original == original_url
        ).first().short, False
    except AttributeError:
        return ''.join([
            choice(ascii_letters + digits) for _ in range(6)
        ]), True


def _get_unique_random_url(original_url):
    while True:
        unique_url, created = _get_random_url(original_url)
        if not created or URLMap.query.filter(
                URLMap.short == unique_url
        ).count() == 0:
            break
    return unique_url, created


def process_data(data):
    data = validate_urls(data)
    if CUSTOM_URL not in data or not data[CUSTOM_URL]:
        data[SHORT_LINK], created = _get_unique_random_url(data[URL])
    else:
        data[SHORT_LINK] = data[CUSTOM_URL]
        created = True
    if CUSTOM_URL in data:
        del data[CUSTOM_URL]
    if created:
        _save_urls(data[URL], data[SHORT_LINK])
    data[SHORT_LINK] = BASE_URL + data[SHORT_LINK]
    return data


def get_original_url(short_url):
    try:
        return URLMap.query.filter(URLMap.short == short_url).first().original
    except AttributeError:
        raise ValidationError('Указанный id не найден', 404)
