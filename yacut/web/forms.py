from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import Length, URL, InputRequired

from yacut.settings import URL_ALLOWED_LENGTH

ORIGINAL_LINK_NAME = 'Длинная ссылка'
INCORRECT_LINK = 'Некорректная ссылка'
REQUIRED_FIELD = 'Поле обязательное'
CUSTOM_ID_NAME = 'Ваш вариант короткой ссылки'
LENGTH_ERROR = 'Длина от 0 до 16'
SUBMIT_BUTTON_TEXT = 'Создать'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_NAME,
        (
            URL(message=INCORRECT_LINK),
            InputRequired(message=REQUIRED_FIELD),
        ),
    )
    custom_id = StringField(
        CUSTOM_ID_NAME,
        (
            Length(0, URL_ALLOWED_LENGTH, LENGTH_ERROR),
        ),
    )
    submit = SubmitField(SUBMIT_BUTTON_TEXT)
