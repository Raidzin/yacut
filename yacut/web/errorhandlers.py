from flask import render_template, flash

from yacut import app
from yacut.web.exceptions import PageNotFound


@app.errorhandler(404)
@app.errorhandler(PageNotFound)
def page_not_found(error):
    return render_template('404.html'), 404
