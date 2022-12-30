from flask import render_template, redirect

from yacut import app
from yacut.settings import BASE_URL
from yacut.web.forms import URLForm
from yacut.web.handlers import get_short_url, get_original_url


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    short_link = (
        BASE_URL + get_short_url(form)
        if form.validate_on_submit()
        else None
    )
    return render_template('index.html', short_link=short_link, form=form)


@app.route('/<url>')
def redirect_to_original_url(url):
    return redirect(get_original_url(url))
