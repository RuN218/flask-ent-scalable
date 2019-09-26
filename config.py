import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = b"\xd6\x01\xea\xce\xff\xc2w\xa3\xc2\x1d\xda\xee\xb5f\x93i\xf1^OV\xcc\xc6D\x83"
    RECAPTCHA_PUBLIC_KEY = "6LdqeroUAAAAAG0vQ4eMKcVmOTzndjg0VlyrSmvs"
    RECAPTCHA_PRIVATE_KEY = '6LdqeroUAAAAAPzRWc033xd6tKbOM3npKEQPQiMl'
    POSTS_PER_PAGE = 10

    TWITTER_API_KEY = "XXXX"
    TWITTER_API_SECRET = "XXXX"
    FACEBOOK_CLIENT_ID = "XXX"
    FACEBOOK_CLIENT_SECRET = "XXXX"


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "database.db")


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "database.db")
