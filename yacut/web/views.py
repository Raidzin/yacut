from flask import render_template, redirect

from yacut import app
from yacut.web.handlers import get_short_url, get_original_url_web
from yacut.web.forms import URLForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        short_link = get_short_url(form)
        return render_template('index.html', short_link=short_link, form=form)
    return render_template('index.html', form=form)


@app.route('/<url>')
def redirect_to_original_url(url):
    return redirect(get_original_url_web(url))
