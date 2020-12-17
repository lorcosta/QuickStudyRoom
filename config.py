from datetime import timedelta
from os import getenv, path
from devkit import set_env

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    FLASKY_ADMIN = getenv('FLASKY_ADMIN')  # ?? what is it
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


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'DEV.db')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')


config = {
    'development': DevConfig,
    'production': ProdConfig
}


def set_config(select=False):
    # if select:
        # return config[set_env(config_menu())]
    return config[set_env(sel_key='d')]
