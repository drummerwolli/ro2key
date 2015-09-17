FROM zalando/python:3.4.0-4
MAINTAINER Teng Qiu <teng.qiu@zalando.de>

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY swagger.yaml /
COPY app.py /
RUN chmod 777 /app.py

WORKDIR /
CMD uwsgi --http :8080 -w app
