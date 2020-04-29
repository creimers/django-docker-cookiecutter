FROM python:3.6

ADD . /project
WORKDIR /project

RUN pip install --upgrade pip pip-tools
RUN pip-compile --rebuild --output-file requirements.txt requirements.in
RUN pip install -r requirements.txt