
FROM python:3.7-alpine


EXPOSE $CV3_PORT

WORKDIR /usr/src/app


COPY requirements.txt ./
RUN apk update
RUN apk upgrade

RUN apk add musl-dev libffi-dev openssl-dev python3-dev make gcc
RUN apk add bash
RUN pip install -r requirements.txt

COPY . .


CMD fab builddocker


