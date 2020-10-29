FROM python:3.8

ADD . /project
WORKDIR /project

RUN pip install --upgrade pip pip-tools
RUN pip install -r requirements.txt