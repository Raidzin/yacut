from yacut.models import URLMap
from yacut.api.exceptions import ProcessingError, ValidationError
from yacut.api.validators import validate_urls

ORIGINAL_URL = 'url'
SHORT_LINK = 'short_link'
CUSTOM_URL = 'custom_id'
BASE_URL = 'http://localhost/'


def process_data(data):
    try:
        data = validate_urls(data)
    except ValidationError as error:
        raise ProcessingError(error.message)
    if CUSTOM_URL not in data or not data[CUSTOM_URL]:
        data[SHORT_LINK] = URLMap.make_sort_url(data[ORIGINAL_URL])
    else:
        data[SHORT_LINK] = data[CUSTOM_URL]
        URLMap.save_urls(data[ORIGINAL_URL], data[SHORT_LINK])
    if CUSTOM_URL in data:
        del data[CUSTOM_URL]
    data[SHORT_LINK] = BASE_URL + data[SHORT_LINK]
    return data


def get_original_url(short_url):
    original_url = URLMap.get_original_ulr(short_url)
    if original_url:
        return original_url
    raise ProcessingError('Указанный id не найден', 404)
