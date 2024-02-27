import os
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY='CLAVE SECRETA'
    SESSION_COOKIE_SECURE=False

class DevelomentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:Hernandexz2001@127.0.0.1/IDGS802'