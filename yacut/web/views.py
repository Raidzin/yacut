from flask import render_template, redirect, url_for

from yacut import app
from yacut.models import URLMap
from yacut.web.exceptions import URLError, PageNotFound
from yacut.web.forms import URLForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        short_url = url_for(
            'redirect_to_original_url',
            _external=True,
            url=URLMap.make_short_url(
                form.original_link.data,
                form.custom_id.data
            ),
        )
        return render_template('index.html', short_link=short_url, form=form)
    except URLMap.DBError as error:
        raise URLError(form, error, 400)


@app.route('/<url>')
def redirect_to_original_url(url):
    original_url = URLMap.get_original_url(url)
    if not original_url:
        raise PageNotFound()
    return redirect(original_url)
