
from celery import Celery


app = Celery(
    'app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['app.tasks']
)


if __name__ == '__main__':
    app.start()
