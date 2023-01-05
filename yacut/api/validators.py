from yacut.api.exceptions import ValidationError
from yacut.settings import (
    ORIGINAL_URL_LENGTH, URL_ALLOWED_LENGTH,
    URL_ALLOWED_CHARACTERS
)
from yacut.models import URLMap

URL = 'url'
CUSTOM_URL = 'custom_id'

EMPTY_DATA = 'Отсутствует тело запроса'
REQUIRED_FIELD = '"url" является обязательным полем!'
INCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'
NAME_REQUIRED = 'Имя "{}" уже занято.'


def _not_none_validation(data):
    if data is None:
        raise ValidationError(EMPTY_DATA)


def _required_object_validation(required_object, data):
    if required_object not in data:
        raise ValidationError(REQUIRED_FIELD)


def _length_validation(allowed_length, data):
    if len(data) > allowed_length:
        raise ValidationError(INCORRECT_NAME)


def _characters_validation(allowed_characters, data):
    if set(data) - allowed_characters:
        raise ValidationError(INCORRECT_NAME)


def _short_url_exist_validation(short_url):
    if URLMap.short_url_exists(short_url):
        raise ValidationError(NAME_REQUIRED.format(short_url))


def _custom_url_validation(custom_url):
    _length_validation(URL_ALLOWED_LENGTH, custom_url)
    _characters_validation(URL_ALLOWED_CHARACTERS, custom_url)
    _short_url_exist_validation(custom_url)


def validate_urls(urls: dict):
    _not_none_validation(urls)
    _required_object_validation(URL, urls.keys())
    _length_validation(ORIGINAL_URL_LENGTH, urls[URL])
    if CUSTOM_URL in urls and urls[CUSTOM_URL]:
        _custom_url_validation(urls[CUSTOM_URL])
    return urls
