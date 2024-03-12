FROM python:3.12

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/media
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip -r requirements.txt 
ADD . /code/

## set display port to avoid crash
ENV DISPLAY=:99

