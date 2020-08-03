import os

from flask import Flask, send_from_directory
from flask_restx import Api, Resource
from rq.job import Job
from werkzeug.middleware.proxy_fix import ProxyFix
from rq import Queue
from worker import conn
from tasks import parsing


if not os.path.exists('./static'):
    os.mkdir('./static')


app = Flask(__name__, static_url_path='/static/', static_folder='../static')
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Parse API',  description='Test API')


q = Queue(connection=conn)


parser_ns = api.namespace('parse', description='Parsing')
results_ns = api.namespace('results', description='Get results')


@parser_ns.route('/post/<string:url>')
@parser_ns.param('url', 'URL для парсинга')
@parser_ns.response(200, 'Ok')
@parser_ns.response(500, 'Server error')
class PostParseTask(Resource):
    def post(self, url):
        """Добавление нового URL в задания для парсинга. URL в формате example.com"""

        job = q.enqueue_call(func=parsing, args=(url,), result_ttl=5000)
        id = job.get_id()
        return id


@parser_ns.route('/<string:id>')
@parser_ns.param('id', 'Идентификатор записи')
class ParsingResult(Resource):

    def get(self, id):
        """Получение результата парсинга по идентификатору"""

        job = Job.fetch(id, connection=conn)
        if job.get_status() == 'finished':
            return f'http://localhost:8888/results/{id}'
        else:
            return 'pending'


@results_ns.route('/<string:id>')
@results_ns.param('id', 'Идентификатор записи')
class Result(Resource):

    def get(self, id):
        """Скачивание файла с результатами парсинга"""

        file_name = f'{id}.html'
        return send_from_directory('static/', file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
