from flask import render_template, flash

from yacut import app
from yacut.web.exceptions import URLError, PageNotFound


@app.errorhandler(404)
@app.errorhandler(PageNotFound)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(URLError)
def api_error(error: URLError):
    if error.status_code == 500:
        return render_template('500.html'), 500
    flash(error.message)
    return render_template('index.html', form=error.form)
