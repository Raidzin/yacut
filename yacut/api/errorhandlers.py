from flask import jsonify

from yacut import app
from yacut.api.exceptions import ProcessingError


@app.errorhandler(ProcessingError)
def validation_error(error: ProcessingError):
    return jsonify(error.to_dict()), error.status_code
