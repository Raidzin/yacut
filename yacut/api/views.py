from flask import jsonify, request

from yacut import app
from yacut.api.utils import process_data, get_original_url


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = process_data(request.get_json())
    return jsonify(data), 201


@app.route('/api/id/<url>/', methods=['GET'])
def get_url(url):
    return jsonify({
        'url': get_original_url(url)
    })
