FROM python:3

RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev

COPY . /api
WORKDIR /api

# install requirements
RUN pip install -r requirements.txt

# run celery worker
ENTRYPOINT ["celery", "-A",  "app.celery",  "worker", "--loglevel=info"]