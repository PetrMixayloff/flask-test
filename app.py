import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Namespace
from rq import Queue
from api.worker import conn
from loguru import logger


if not os.path.exists('./static'):
    os.mkdir('./static')


app = Flask(__name__, static_url_path='/static/', static_folder='../static')
CORS(app)


app.config.from_object('config.Development')

db_session = db = SQLAlchemy(app)

q = Queue(connection=conn)

logger.remove()
logger.add("log.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
logger.add(sys.stdout, colorize=True, format="<green> {time:YYYY-MM-DD at HH:mm:ss} </green> | {level} | {message}")

api = Api(title='test parser',
          version='1.0',
          description='Тест парсер')

prefix = '/api'

parser_ns = Namespace('Парсинг', description='Парсинг')

api.add_namespace(parser_ns, path=prefix + '/parser')


if __name__ == '__main__':
    api.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
