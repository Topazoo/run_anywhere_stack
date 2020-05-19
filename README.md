# Web Stack

## Overview:

A dead simple Dockerized stack for web and native mobile applications:

Backend:

[dead_simple_framework](https://github.com/Topazoo/dead_simple_framework): Flask + MongoDB + Celery


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

## Current Demo:

- An auto-configured [backend](https://github.com/Topazoo/web-stack/blob/master/server/app/server_demo.py) that:
  - Runs a chain of celery tasks (simple addition then a MongoDB insert to the `insert` collection every 60 seconds)
  - Supports CRUD operations [GET, POST, PUT, DELETE] on `/demo` and `/insert`
  - Fires a Celery task on `/`

- A fully platform-agnostic frontend that:
  - Calls `/insert` to retreive the data in the `insert` collection and renders in a scrollable list
  