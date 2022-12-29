from flask import render_template, flash

from yacut import app
from yacut.web.exceptions import APIError, PageNotFound


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(PageNotFound)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(APIError)
def api_error(error: APIError):
    if error.status_code == 500:
        return render_template('500.html'), 500
    flash(error.message)
    return render_template('index.html', user_input=error.user_input)
