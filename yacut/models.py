from datetime import datetime
from random import choices

from sqlalchemy.exc import IntegrityError

from yacut import db
from yacut.settings import (
    URL_ALLOWED_CHARACTERS, RANDOM_RETRIES,
    ORIGINAL_URL_LENGTH, URL_ALLOWED_LENGTH,
)

MAX_RETRIES = 'Не удалось создать уникальную ссылку'
NAME_REQUIRED = 'Имя {} уже занято!'


class URLMap(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    original = db.Column(
        db.String(ORIGINAL_URL_LENGTH),
        nullable=False,
    )
    short = db.Column(
        db.String(URL_ALLOWED_LENGTH),
        unique=True, nullable=False,
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
    )

    def _save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save_urls(cls, original, short):
        url_map = URLMap(original=original, short=short)
        url_map._save()

    @staticmethod
    def get_short_url_from_original(original_url):
        url_map = URLMap.query.filter(
            URLMap.original == original_url
        ).first()
        if url_map:
            return url_map.short
        return None

    @staticmethod
    def get_short_url(short_url):
        return URLMap.query.filter(URLMap.short == short_url).first()

    @staticmethod
    def get_original_url(short_url):
        # if urlmap := URLMap.get_short_url(short_url):
        #     return urlmap.original
        # return None
        urlmap = URLMap.get_short_url(short_url)
        if urlmap:
            return urlmap.original
        return None

    @classmethod
    def get_unique_url(cls):
        for _ in range(RANDOM_RETRIES):
            unique_url = ''.join(choices([*URL_ALLOWED_CHARACTERS], k=6))
            if URLMap.query.filter(URLMap.short == unique_url).count() == 0:
                return unique_url
        raise TimeoutError(MAX_RETRIES)

    @staticmethod
    def make_random_short_url(original_url):
        short_url = URLMap.get_short_url_from_original(original_url)
        if short_url is None:
            try:
                short_url = URLMap.get_unique_url()
            except TimeoutError as error:
                raise URLMap.DBError(error)
            URLMap.save_urls(original_url, short_url)
        return short_url

    @staticmethod
    def make_short_url(original_url, short_url=None):
        if not short_url:
            return URLMap.make_random_short_url(original_url)
        try:
            URLMap.save_urls(original_url, short_url)
        except IntegrityError:
            raise URLMap.DBError(NAME_REQUIRED.format(short_url))
        return short_url

    @staticmethod
    def short_url_exists(url):
        return bool(URLMap.get_short_url(url))

    class DBError(Exception):
        pass
