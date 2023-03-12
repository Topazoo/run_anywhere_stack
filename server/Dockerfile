# Server Build
FROM python:3.9-alpine
LABEL maintainer="Peter Swanson | pswanson@ucdavis.edu"

WORKDIR /app
COPY /app ./

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev build-base python3-dev rust cargo

COPY setup/requirements.txt /app/setup/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r setup/requirements.txt

CMD ["gunicorn", "main:gunicorn", "-w 2", "-b 0.0.0.0:5000", "-t 30"]