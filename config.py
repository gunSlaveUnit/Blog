import os

from dotenv import dotenv_values

config = dotenv_values('.env')


class Config(object):
    SECRET_KEY = config["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = config["SQLALCHEMY_DATABASE_URI"]
    MAIL_SERVER = config["MAIL_SERVER"]
    MAIL_PORT = config["MAIL_PORT"]
    MAIL_USE_TLS = config["MAIL_USE_TLS"]
    MAIL_USERNAME = config["MAIL_USERNAME"]
    MAIL_PASSWORD = config["MAIL_PASSWORD"]
