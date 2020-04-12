FROM python:3.7-alpine

LABEL maintainer="Peter Swanson | pswanson@ucdavis.edu"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app/main.py" ]