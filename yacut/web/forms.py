from re import compile, escape

from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import Length, URL, InputRequired, Regexp

from yacut.settings import (
    ORIGINAL_URL_LENGTH, URL_ALLOWED_LENGTH,
    URL_ALLOWED_CHARACTERS
)

ORIGINAL_LINK_NAME = 'Длинная ссылка'
INCORRECT_LINK = 'Некорректная ссылка'
REQUIRED_FIELD = 'Поле обязательное'
CUSTOM_ID_NAME = 'Ваш вариант короткой ссылки'
LENGTH_ERROR = 'Длина должна быть до {}'
ORIGINAL_URL_LENGTH_ERROR = LENGTH_ERROR.format(ORIGINAL_URL_LENGTH)
URL_LENGTH_ERROR = LENGTH_ERROR.format(URL_ALLOWED_LENGTH)
INCORRECT_URL = 'Ссылка должна содержать только латинские символы и цифры'
SUBMIT_BUTTON_TEXT = 'Создать'

ALLOWED_CHARACTERS_REGEX = compile(rf'^[{escape(URL_ALLOWED_CHARACTERS)}]*$')


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_NAME,
        (
            InputRequired(message=REQUIRED_FIELD),
            Length(max=ORIGINAL_URL_LENGTH, message=ORIGINAL_URL_LENGTH_ERROR),
            URL(message=INCORRECT_LINK),
        ),
    )
    custom_id = StringField(
        CUSTOM_ID_NAME,
        (
            Length(max=URL_ALLOWED_LENGTH, message=URL_LENGTH_ERROR),
            Regexp(ALLOWED_CHARACTERS_REGEX, message=INCORRECT_URL),
        ),
    )
    submit = SubmitField(SUBMIT_BUTTON_TEXT)
