# pull the python:3.11-slim-buster image
FROM python:3.11-slim-buster AS base

# create working directory in docker
WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get -y install python3-dev \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt

# copy file 'here' to docker working directory
COPY . /backend
