from datetime import datetime
from random import choice

from yacut import db
from yacut.settings import URL_ALLOWED_CHARACTERS, RANDOM_RETRIES


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(100), nullable=False)
    short = db.Column(db.String(6), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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
    def get_original_ulr(short_url):
        try:
            return URLMap.query.filter(
                URLMap.short == short_url
            ).first().original
        except AttributeError:
            return None

    @staticmethod
    def _get_random_url():
        return ''.join([
            choice(URL_ALLOWED_CHARACTERS) for _ in range(6)
        ])

    @classmethod
    def get_unique_url(cls):
        for _ in range(RANDOM_RETRIES):
            unique_url = cls._get_random_url()
            if URLMap.query.filter(URLMap.short == unique_url).count() == 0:
                return unique_url
        raise OverflowError

    @classmethod
    def make_sort_url(cls, original_url):
        short_url = cls.get_short_url_from_original(original_url)
        if short_url is None:
            short_url = cls.get_unique_url()
        cls.save_urls(original_url, short_url)
        return short_url

    @staticmethod
    def short_url_exists(url):
        return not URLMap.query.filter(URLMap.short == url).count() == 0
