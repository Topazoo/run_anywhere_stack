FROM python:3.7-alpine

LABEL maintainer="Peter Swanson | pswanson@ucdavis.edu"

WORKDIR /app
COPY . /app

ENV FLASK_APP app/main.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app/main.py" ]