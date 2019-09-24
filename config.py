import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = b"\xd6\x01\xea\xce\xff\xc2w\xa3\xc2\x1d\xda\xee\xb5f\x93i\xf1^OV\xcc\xc6D\x83"
    POSTS_PER_PAGE = 10


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "database.db")


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "database.db")
