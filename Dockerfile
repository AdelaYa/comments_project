FROM python:3.8


ENV PYTHONUNBUFFERED 1

RUN mkdir /blog

WORKDIR /blog

ADD requirements.txt /blog/
RUN pip install -r requirements.txt

