# Server Build
FROM python:3.9-slim-buster as build

LABEL maintainer="Peter Swanson | pswanson@ucdavis.edu"

WORKDIR /app
COPY /app ./

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

COPY setup/requirements.txt /app/setup/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libffi-dev libssl-dev python3-dev rustc cargo && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r setup/requirements.txt && \
    apt-get remove -y build-essential gcc libffi-dev libssl-dev python3-dev rustc cargo && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Final image
FROM python:3.9-slim-buster

COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

CMD [ "python", "scheduler_demo.py" ]