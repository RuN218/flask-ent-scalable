class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 10


class ProdConfig(Config):
    SECRET_KEY = b"\xd6\x01\xea\xce\xff\xc2w\xa3\xc2\x1d\xda\xee\xb5f\x93i\xf1^OV\xcc\xc6D\x83"


class DevConfig(Config):
    SECRET_KEY = b"6X$\x8bQ\xbe\xb2\x81\x90}\xb7\xf0\x13,\x13\x9bBM,M4\x85\xbb\x89"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
