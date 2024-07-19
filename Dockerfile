FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/media
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip -r requirements.txt 
RUN pip3 install gunicorn
ADD . /code/

## set display port to avoid crash
ENV DISPLAY=:99

