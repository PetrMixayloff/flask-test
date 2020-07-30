# coding: utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

db_params = dict(user='db_user',
                 passw='12345678',
                 host='localhost',
                 port=5432)

database_name = 'db_name'
local_base = 'postgresql://{user}:{passw}@{host}:{port}/'.format(user=db_params['user'],
                                                                 passw=db_params['passw'],
                                                                 host=db_params['host'],
                                                                 port=db_params['port'])


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '077fb320-6dc1-4033-a8b0-5ba0a55dceb2')
    APP_UUID = 'fa7d5d7a-5179-4b48-a864-a42661e814a1'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = local_base + database_name
    RESTPLUS_MASK_HEADER = False
    RESTPLUS_MASK_SWAGGER = False
    FILE_UPLOAD_FOLDER = "files"
    SECRET_TO_SIGN_TASK = '123456'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class Development(BaseConfig):
    """Development configuration."""
    DEBUG = True


class Production(BaseConfig):
    """Production configuration."""
    pass
