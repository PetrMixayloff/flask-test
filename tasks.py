import requests
from rq import get_current_job


HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}
TIMEOUT = 5


def parsing(url: str):
    job = get_current_job()
    task_id = job.get_id()
    url = 'http://' + url
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    with open(f'static/{task_id}.html', 'w') as f:
        f.write(r.text)
