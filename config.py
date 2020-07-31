# coding: utf-8
import os


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '077fb320-6dc1-4033-a8b0-5ba0a55dceb2')
    APP_UUID = 'fa7d5d7a-5179-4b48-a864-a42661e814a1'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    USER = 'db_parse_user'
    PASSWORD = 'db_parse_user_pass'
    HOST = 'localhost'
    PORT = 5432
    DB_NAME = 'db_parse'
    SQLALCHEMY_DATABASE_URI = local_base = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    RESTPLUS_MASK_HEADER = False
    RESTPLUS_MASK_SWAGGER = False
    FILE_UPLOAD_FOLDER = "files"
    SECRET_TO_SIGN_TASK = '123456'


class Development(BaseConfig):
    """Development configuration."""
    DEBUG = True
    ASSETS_DEBUG = True


class Production(BaseConfig):
    """Production configuration."""
    pass
