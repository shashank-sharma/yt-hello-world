FROM python:3

RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev

COPY . /api
WORKDIR /api

# install requirements
RUN pip install -r requirements.txt

# expose the app port
EXPOSE 5000

RUN chmod +x start.sh