# pull official base image
FROM python:3.8-alpine3.13

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add build-base libffi-dev openssl-dev \
    && apk add postgresql-dev

# copy entire project directory
COPY . .

RUN pip install pipenv
RUN pipenv install --system

# sasori in Naruto is our default user
RUN adduser -D sasori
USER sasori