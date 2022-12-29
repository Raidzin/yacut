from os.path import join
from os import getenv, getcwd

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
cwd = getcwd()


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')


app = Flask(
    __name__,
    template_folder=join(cwd, 'html'),
    static_url_path='',
    static_folder=join(cwd, 'html'),
)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
