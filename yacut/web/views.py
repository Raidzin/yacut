from flask import render_template, request, redirect

from yacut import app
from yacut.web.handlers import get_short_url, get_original_url
from yacut.web.exceptions import APIError


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    api_request = request.form.to_dict()
    api_request['url'] = api_request['original_link']
    del api_request['original_link']
    short_link = get_short_url(api_request)
    return render_template('index.html', short_link=short_link)


@app.route('/<url>')
def redirect_to_original_url(url):
        return redirect(get_original_url(url))

