FROM python:3.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

WORKDIR /pybuilder-anybadge

COPY . /pybuilder-anybadge/

# RUN apk --update --no-cache add gcc libc-dev libffi-dev openssl-dev
RUN pip install pybuilder==0.11.17
# RUN pyb install_dependencies
# RUN pyb install
