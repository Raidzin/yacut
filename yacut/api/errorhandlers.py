from flask import jsonify

from yacut import app
from yacut.api.exceptions import ValidationError


@app.errorhandler(ValidationError)
def validation_error(error: ValidationError):
    return jsonify(error.to_dict()), error.status_code
