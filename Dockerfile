FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /pybuilder-anybadge

COPY . /pybuilder-anybadge/

RUN pip install pybuilder
RUN pyb
