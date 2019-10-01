import os

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = b"\xd6\x01\xea\xce\xff\xc2w\xa3\xc2\x1d\xda\xee\xb5f\x93i\xf1^OV\xcc\xc6D\x83"
    RECAPTCHA_PUBLIC_KEY = "XXXX"
    RECAPTCHA_PRIVATE_KEY = 'XXXX'
    POSTS_PER_PAGE = 10

    TWITTER_API_KEY = "XXXX"
    TWITTER_API_SECRET = "XXXX"
    FACEBOOK_CLIENT_ID = "XXX"
    FACEBOOK_CLIENT_SECRET = "XXXX"

    CELERY_IMPORTS = ("webapp.blog.tasks",)
    CELERY_BROKER_URL = "amqp://rabbitmq:rabbitmq@localhost//"
    CELERY_RESULT_BACKEND = "amqp://rabbitmq:rabbitmq@localhost//"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USER = "XXXX"
    MAIL_PASSWORD = "XXXX"
    MAIL_DEFAULT_SENDER = "from@flask.com"

    CELERY_SCHEDULE = {
        "weekly-digest": {
            "task": "blog.tasks.digest",
            "schedule": crontab(day_of_week=6, hour="10")
        },
    }

    LANGUAGES = ["en", "ru"]


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "database.db")

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = '0'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "database.db")

    CACHE_TYPE = "simple"


class TestConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "null"
    WTF_CSRF_ENABLED = False

    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"

    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USER = "username"
    MAIL_PASSWORD = "password"
