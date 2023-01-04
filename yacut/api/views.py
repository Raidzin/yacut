from flask import jsonify, request

from yacut import app
from yacut.models import URLMap
from yacut.settings import BASE_URL
from yacut.api.validators import validate_urls
from yacut.api.exceptions import ValidationError, ProcessingError

URL_NOT_FOUND = 'Указанный id не найден'

ORIGINAL_URL = 'url'
SHORT_LINK = 'short_link'
CUSTOM_URL = 'custom_id'


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    try:
        data = validate_urls(request.get_json())
        if CUSTOM_URL not in data or not data[CUSTOM_URL]:
            short_link = URLMap.make_random_short_url(data[ORIGINAL_URL])
        else:
            short_link = data[CUSTOM_URL]
            URLMap.save_urls(data[ORIGINAL_URL], short_link)
        short_link = BASE_URL + short_link
        return jsonify({
            ORIGINAL_URL: data[ORIGINAL_URL],
            SHORT_LINK: short_link
        }), 201
    except ValidationError as error:
        raise ProcessingError(error.message)
    except URLMap.DBError as error:
        raise ProcessingError(error)


@app.route('/api/id/<short_url>/', methods=['GET'])
def get_url(short_url):
    if not (original_url := URLMap.get_original_url(short_url)):
        raise ProcessingError(URL_NOT_FOUND, 404)
    return jsonify({
        ORIGINAL_URL: original_url
    })
