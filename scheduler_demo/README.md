# Backend with Scheduler Demo

## Overview:

Demos a simple application with some automatic CRUD routes and some of the
task scheduling and parallelization capabilities.

Backend:

[dead_simple_framework](https://github.com/Topazoo/dead_simple_framework): Flask + MongoDB + Celery

## Running the demo server:

1. Pull the code:

```sh
git clone https://github.com/Topazoo/run_anywhere_stack.git
```

2. Build the server and job scheduler:

```sh
$ cd run_anywhere_stack/compose/scheduler_demo
$ docker-compose build --no-cache
```

3. Run the server and job scheduler:

```sh
$ docker-compose up --force-recreate
```

## Current Demo:

- An auto-configured [backend](https://github.com/Topazoo/run_anywhere_stack/blob/master/scheduler_demo/app/scheduler_demo.py) that:
  - Runs a chain of celery tasks (simple addition then a MongoDB insert to the `insert` collection every 60 seconds)
  - Supports CRUD operations [GET, POST, PUT, DELETE] on `/insert`
  - Fires a Celery task on:
    - `/add?x=<x>&y=<y>` - Adds together two numbers as a task
    - `/refresh` - Fires a series of API calls to load random zipcode data
  - Returns the cached task result of `/refresh` on `/`
