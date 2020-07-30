import requests
from api.models import Tasks
from api.utils import getById
from app import db_session


HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}
TIMEOUT = 5


def parsing(url: str, task_id: str):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    with open(f'../static/{task_id}.html', 'w') as f:
        f.write(r.text)
    task = getById(Tasks, task_id, db_session.session)
    task.status = 'done'
    db_session.session.query(Tasks).filter(Tasks.id == task.id).update(task.__dict__)
    db_session.session.commit()
