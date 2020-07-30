# -*- coding: utf-8 -*-
from flask import abort
from flask_restplus import Resource
from api.models import Tasks
from api.utils import getById
from api.tasks import parsing
from app import logger, db_session, q, parser_ns as api

import uuid
import traceback


@api.route('/')
@api.param('url', 'URL для парсинга')
@api.response(200, 'Success')
@api.response(400, 'Validation error')
@api.response(500, 'Error')
class Task(Resource):
    @api.doc()
    def post(self, url):
        """Добавление нового задания"""

        id_ = str(uuid.uuid4())
        q.enqueue_call(func=parsing, args=(url, id_), result_ttl=5000)

        try:
            db_session.session.add(Tasks(id=id_, task=url))
            db_session.session.commit()
        except Exception as ex:
            logger.error(traceback.format_exc())
            message = 'ERROR 500 сервера: ' + str(ex)
            return abort(500, message)
        return id_


@api.route('/<uuid:id_>')
@api.param('id_', 'Идентификатор записи')
@api.response(200, 'Success')
@api.response(400, 'Validation error')
@api.response(500, 'Error')
class ParsingResult(Resource):

    def get(self, id_):
        """Получение результата парсинга по идентификатору"""

        try:
            entity = getById(Tasks, id_, db_session.session)
        except Exception as ex:
            logger.error(traceback.format_exc())
            message = 'ERROR 500 сервера: ' + str(ex)
            return abort(500, message)
        if entity.status != 'done':
            return entity.status
        else:
            return entity.result
