# Server Build
FROM python:3.7-alpine
LABEL maintainer="Peter Swanson | pswanson@ucdavis.edu"

WORKDIR /app
COPY . /app

ENV FLASK_APP=app/server_demo.py
ENV CELERY_APP_NAME=server_demo
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache -r requirements.txt

CMD [ "python", "server_demo.py" ]