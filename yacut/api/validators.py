from string import ascii_letters, digits

from yacut.models import URLMap
from yacut.api.exceptions import ValidationError

URL = 'url'
CUSTOM_URL = 'custom_id'

ALLOWED_URL_LENGTH = 16
EMPTY_DATA = 'Отсутствует тело запроса'
REQUIRED_FIELD = '"url" является обязательным полем!'
INCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'
NAME_REQUIRED = 'Имя "{}" уже занято.'


def _check_url_in_database(url):
    a = URLMap.query.filter(URLMap.short == url).count()
    print(a)
    return not URLMap.query.filter(URLMap.short == url).count() == 0


def validate_urls(urls: dict):
    if urls is None:
        raise ValidationError(EMPTY_DATA)
    if URL not in urls.keys():
        raise ValidationError(REQUIRED_FIELD)
    if CUSTOM_URL not in urls or not urls[CUSTOM_URL]:
        return urls
    custom_url = urls[CUSTOM_URL]
    if (
        len(str(custom_url)) > ALLOWED_URL_LENGTH
        or set(custom_url) - set(ascii_letters + digits)
    ):
        raise ValidationError(INCORRECT_NAME)
    if _check_url_in_database(custom_url):
        raise ValidationError(NAME_REQUIRED.format(custom_url))
    return urls
