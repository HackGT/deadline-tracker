FROM python:alpine

ADD . /src

WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 5000
CMD FLASK_APP=app/server.py python -m flask run --host 0.0.0.0

