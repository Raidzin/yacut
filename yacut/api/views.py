from flask import jsonify, request, url_for

from yacut import app
from yacut.models import URLMap
from yacut.settings import REDIRECT_FUNCTION_NAME
from yacut.api.exceptions import ProcessingError, ValidationError
from yacut.api.validators import validate_urls

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
        short_link = url_for(
            REDIRECT_FUNCTION_NAME,
            _external=True,
            url=short_link,
        )
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
    original_url = URLMap.get_original_url(short_url)
    if not original_url:
        raise ProcessingError(URL_NOT_FOUND, 404)
    return jsonify({
        ORIGINAL_URL: original_url
    })
