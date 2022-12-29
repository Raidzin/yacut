from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField


class URLForm(FlaskForm):
    original_link = URLField('Длинная ссылка')
    custom_id = StringField('Ваш вариант короткой ссылки')
    submit = SubmitField('Создать')
