FROM python:2.7.11
MAINTAINER Frank Hoffsümmer "frank.hoffsummer@gmail.com"
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /code
COPY requirements.txt /code/
WORKDIR /code

RUN pip install -r requirements.txt
