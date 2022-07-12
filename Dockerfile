FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /ChatApi

WORKDIR /ChatApi

COPY . /ChatApi/

RUN pip install --upgrade pip && pip install pip-tools && pip install -r requirements.txt 