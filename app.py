import os
import sys
import traceback
import datetime

from flask import Flask, abort
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from rq import Queue
from worker import conn
from tasks import parsing
from loguru import logger
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


if not os.path.exists('./static'):
    os.mkdir('./static')


app = Flask(__name__, static_url_path='/static/', static_folder='../static')
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Parse API',  description='Test API')


app.config.from_object('config.Development')

db_session = db = SQLAlchemy(app)

q = Queue(connection=conn)

logger.remove()
logger.add("log.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
logger.add(sys.stdout, colorize=True, format="<green> {time:YYYY-MM-DD at HH:mm:ss} </green> | {level} | {message}")

parser_ns = api.namespace('Parse', description='Parsing')


def getById(model, _id, session):
    """
    общий метод получения сущности по id в базе
    :param model: модель сущности бд
    :param _id: id сущности в базе
    :param session: сессия пула подключений к базе
    :return: сущность или raise Exception
    """

    try:
        entity = session.query(model) \
            .filter(model.id == _id) \
            .one()
        return entity

    except Exception:
        session.rollback()
        raise


class Task(db.Model):
    """ Таблица Результаты парсинга """
    __tablename__ = "task"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    date_created = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())
    task = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    result = db.Column(db.String, nullable=True)


@parser_ns.route('/')
@parser_ns.param('url', 'URL для парсинга')
@parser_ns.response(500, 'Server error')
class PostParseTask(Resource):
    @api.doc()
    def post(self, url):
        """Добавление нового URL в задания для парсинга"""

        id_ = str(uuid4())
        q.enqueue_call(func=parsing, args=(url, id_, Task, db_session), result_ttl=5000)

        try:
            db_session.session.add(Task(id=id_, task=url))
            db_session.session.commit()
        except Exception as ex:
            logger.error(traceback.format_exc())
            message = 'ERROR 500 сервера: ' + str(ex)
            return abort(500, message)
        return id_


@parser_ns.route('/<uuid:id_>')
@parser_ns.param('id_', 'Идентификатор записи')
class ParsingResult(Resource):

    def get(self, id_):
        """Получение результата парсинга по идентификатору"""

        try:
            entity = getById(Task, id_, db_session.session)
        except Exception as ex:
            logger.error(traceback.format_exc())
            message = 'ERROR 500 сервера: ' + str(ex)
            return abort(500, message)
        if entity.status != 'done':
            return entity.status
        else:
            return entity.result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
