# Web Stack

## Overview:

A dead simple Dockerized stack for web and native mobile applications:

Backend:

[dead_simple_framework](https://github.com/Topazoo/dead_simple_framework): Flask + MongoDB + Celery + Docker


Frontend:

[flutter_web_frontend](https://github.com/Topazoo/flutter_web_frontend) : Web + iOS Native + Android Native

## Running the application client and server:

1. Pull the code:

```sh
git clone https://github.com/Topazoo/web-stack.git
```

2. Run the server, client and job scheduler:

```sh
$ cd web-stack
$ docker-compose up --force-recreate
```
