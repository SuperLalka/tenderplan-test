FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./compose/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


COPY . /app
