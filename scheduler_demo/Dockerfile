# Server Build
FROM python:3.9-alpine
LABEL maintainer="Peter Swanson | pswanson@ucdavis.edu"

WORKDIR /app
COPY /app ./
ENV FLASK_APP=scheduler_demo.py
ENV CELERY_APP_NAME=scheduler_demo
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev libressl-dev

COPY setup/requirements.txt /app/setup/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r setup/requirements.txt

CMD [ "python", "scheduler_demo.py" ]