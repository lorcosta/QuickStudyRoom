import os
from datetime import timedelta
from os import getenv, path
from devkit import set_env

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    FLASKY_ADMIN = getenv('FLASKY_ADMIN')
    SECRET_KEY = getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = getenv('MAIL_USERNAME')
    UPLOADED_PHOTOS_DEST = os.getcwd()


class DevConfig(Config):
    DEBUG = True
    THREADED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'DEV.db')
    UPLOADED_PHOTOS_DEST = os.getcwd()

config = {
    'development': DevConfig
}


def set_config():
    return config[set_env(sel_key='d')]
