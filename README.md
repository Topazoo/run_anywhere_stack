# Building the App

- Ensure [Docker](https://docs.docker.com/get-docker/) is installed on your machine
- Ensure [Python3](https://www.python.org/downloads/) is installed on your machine
- Ensure [NodeJS + NPM](https://nodejs.org/en/download/) is installed on your machine


## Backend + Frontend

### Build the application

```sh
$ npm install --prefix ./client/app
$ cd compose/local
$ docker-compose build --no-cache
```

### Create a `.env` file in `compose/local`
With the contents:
```env
REACT_APP_API_URL=http://localhost:5000/
MONGODB_ATLAS=False
APP_USE_JWT=True
USE_SLACK=False
USE_SENTRY=False
APP_JWT_LIFESPAN=1800
```

## Backend

### Build the application

```sh
$ cd compose/local
$ docker-compose build server
```

## Frontend

### Build the application

```sh
$ npm install --prefix ./client/app
$ cd compose/local
$ docker-compose build frontend
```

# Running

## Backend + Frontend

```sh
$ cd compose/local
$ docker-compose up --force-recreate
```

Visit [http://localhost/](http://localhost/)

## Backend Only

```sh
$ cd compose/local
$ docker-compose up --force-recreate server
```

## Frontend Only

```sh
$ cd compose/local
$ docker-compose up --force-recreate frontend
```

Visit [http://localhost/](http://localhost/)

# Running Server-Side Scripts

## Create an initial Admin user

1. Start the server using `docker-compose`
2. Run:
    ```sh
    $ docker exec -it local_server_1 scripts/create_initial_admin.py
    ```
3. An Admin user will be created with the following credentials:
    - email: admin@application.org
    - username: admin@application.org
    - password: Password

# API Documentation Collection

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/8610254-379e4614-3297-40e1-924c-e34cb9e677bb?action=collection%2Ffork&collection-url=entityId%3D8610254-379e4614-3297-40e1-924c-e34cb9e677bb%26entityType%3Dcollection%26workspaceId%3Ddb930828-a68a-4dc0-8e82-c763986bd6eb)

# Task Scheduler Demo:

You can find an additional demo application [scheduler_demo](https://github.com/Topazoo/run_anywhere_stack/blob/master/scheduler_demo/) with an attached README.
This demo application demonstrates the Task Manager and task scheduling capabilities of dead-simple-framework

### Acknowledgments

Many thanks to [Dean](https://github.com/deanmayne) who wrote much of the React code that made it into the early commits of this project.
