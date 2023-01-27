---
Title: Building an SMS Reminder System using FastAPI and Vonage SMS API
description: An SMS reminder system that allows users to text a specific number to set reminders for themselves.
thumbnail: /thumbnail-url/goes-here.png
author: Abram
category: tutorial
tags:
  - python
  - backend
  - fastapi
  - sms-api
---

# Building an SMS Reminder System using FastAPI and Vonage SMS API

In this article, you will learn how to build an sms reminder backend system using Vonage SMS API. Interesting, right? I know, let's jump into it!

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It is built on top of Starlette for the web parts and Pydantic for the data parts. Its advantages are the ability to create endpoints quickly, having built-in support for WebSockets and being asynchronous. I would use Python for the backend system because of its simplicity and scalability as well as its vast ecosystem and libraries that can be used for a wide range of tasks.

> Disclaimer: I would recommend you go through the FastAPI official [documentation](https://fastapi.tiangolo.com/tutorial/) or a video [tutorial](https://www.youtube.com/watch?v=7t2alSnE2-I&t=7s) to get started with the framework; as doing this would help speed things up.

Vonage's SMS API enables you to send and receive text messages to and from users worldwide, using our REST APIs. Get started [here](https://developer.vonage.com/en/messaging/sms/overview#getting-started).

- Programmatically send and receive high volumes of SMS globally.
- Send SMS with low latency and high delivery rates.
- Receive SMS using local numbers.
- Scale your applications with familiar web technologies.
- Pay only for what you use, nothing more.
- Auto-redact feature to protect privacy.

## Vonange Account Setup

To follow along this tutorial, I would strongly advicie that you setup a vonage account. You can start by signing up [here](https://developer.vonage.com/sign-up) and start building with free credit. Once you have, kindly grab your API and Secret key at the top of the vonage api [dashboard](https://dashboard.nexmo.com/).

## Project Setup and Installation

1). Create and Activate The Virtual Environment

To begin, start by creating a directory, a virtual environment (preferrably pipenv) and activate it:

```bash
mkdir sms_reminder && cd sms_reminder
python3.9 -m pipenv shell
```

2). Install Required Dependencies

Create a `requirements.txt` file in the directory and continue by copying and pasting the code snnipet below in your `requirements.txt` file:

```python
aiosqlite==0.18.0
alembic==1.9.2
anyio==3.6.2
apscheduler==3.9.1.post1
certifi==2022.12.7
click==8.1.3
databases==0.7.0
fastapi==0.89.1
greenlet==2.0.1; python_version >= '3' and (platform_machine == 'aarch64' or (platform_machine == 'ppc64le' or (platform_machine == 'x86_64' or (platform_machine == 'amd64' or (platform_machine == 'AMD64' or (platform_machine == 'win32' or platform_machine == 'WIN32'))))))
h11==0.14.0
httpcore==0.16.3
httptools==0.5.0
httpx==0.23.3
idna==3.4
mako==1.2.4
markupsafe==2.1.2
pydantic==1.10.4
python-decouple==3.7
python-dotenv==0.21.1
pytz-deprecation-shim==0.1.0.post0
pytz==2022.7.1
pyyaml==6.0
rfc3986==1.5.0
six==1.16.0
sniffio==1.3.0
sqlalchemy==1.4.46
starlette==0.22.0
typing-extensions==4.4.0
tzdata==2022.7; python_version >= '3.6'
tzlocal==4.2
uvicorn==0.20.0
uvloop==0.17.0
watchfiles==0.18.1
websockets==10.4
```

Proceed to installing the required packages at once using the command below:

```bash
pipenv install -r requirements.txt
```

3). Create `main` Module

Now that you have installed the required dependencies, let's proceed by creating a `main.py` file and pasting the below code into it. This is the entrypoint of the backend system that will be responsible for constructing the FastAPI application, registering API routers, events to connect and disconnect the database, start job schedulers and runnning the application.

```python
# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI


# construct application
app = FastAPI(
    title="SMS Reminder System",
    description="An SMS reminder system that allows users to text a specific number to set reminders for themselves.",
    verison=1.0,
)


@app.on_event("startup")
async def startup():
    pass # connect to database will come here


@app.on_event("shutdown")
async def disconnect():
    pass # disconnect from database will come here


if __name__ == "__main__":
    uvicorn.run(
        "sms_reminder.main:app", host="0.0.0.0", port=3030, reload=True
    )
```

4). Create `models` Directory

We created `main.py`, the entrypoint of our application. Next would be creating the models directory, and basically, what will be there is going to be our database tables defined as class(es). Let's begin, create an `__init__.py` file to inform Python to treat this directory as a module.

> I like to keep my codes clean, because it helps other team members of mine to understand and tell what is going on, and to quickly start contributing or making a fix.

Let's start by creating a `base.py` file, this fill will contain a class named `ObjectTracker`. Basically, this class is a base class for all the objects that will be tracked in the database.

```python
# Stdlib Imports
from datetime import datetime

# SQLAlchemy Imports
from sqlalchemy import Column, Integer, DateTime


class ObjectTracker(object):
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, onupdate=datetime.now)
```

We are importing the `Column`, `Integer`, and `DateTime` classes from the sqlalchemy module to create the base class for tracking objects in the database, and also importing `datetime` from the Python standard library to keep .track of when an object was created or updated.

Next would be creating an `sms.py` file, copy and paste the below code into it:

```python
# SQLAlchemy Imports
from sqlalchemy import Column, String, DateTime

# Own Imports
from sms_reminder.models.base import ObjectTracker


class Reminder(ObjectTracker):

    phone_number = Column(String)
    message = Column(String)
    remind_when = Column(DateTime)
```

The `Reminder` class is going to be a representation of the `reminders` table in our database. But in order for us to convert this object into a class that would be translated into a database table we need to configure our database.

5). Create `config` Directory

Remember that we need to tell Python to treat this directory as a module, so we begin by creating an `__init__.py` file. Next would be creating a `database.py` file, this will hold information about configuring the database, engine, constructing a session maker, a database connector (to connect and shutdown our database) and creating a declarative base class that would help convert our models into database table.

Let's proceed; continue by copying below code and paste it into the `database.py` file:

```python
# SQLAlchemy Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Third Imports
from databases import Database


# create database and engine
DATABASE_URL = "sqlite:///./sms_reminder.sqlite"
DATABASE_ENGINE = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# construct a session maker
session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=DATABASE_ENGINE
)

# construct a scoped session
SessionLocal = scoped_session(session_factory)

# Construct a base class for declarative class definitions
Base = declarative_base()

# Construct a db connector to connect, shutdown database
db_connect = Database(DATABASE_URL)
```

You must be thinking "woah, things are getting pretty complex already"? Don't worry about it, I'll explain to you the magic you are seeing.

- `create_engine`: basically, this method is taking in the connection (database) URL and rreturning a sqlachemy engine that references both a Dialect and a Pool, which together interpret the DBAPI's module functions as well as the behavior of the database ([Source](https://www.geeksforgeeks.org/connecting-to-sql-database-using-sqlalchemy-in-python/#:~:text=The%20create_engine()%20method%20of,the%20behavior%20of%20the%20database.)).
- `session_maker`: to explain this, we need to start by understanding what a `Session` is. A Session in sqlalchemy establishes alll conversations with the database, it is a regular python class which can directly be instantiated. The `session_maker` is used to create a top-level `Session` configuration which can then be used throughout an application without the need to repeat certain configurational arguments. Read more [here](https://www.geeksforgeeks.org/sqlalchemy-orm-creating-session/) and [here](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-make-a-sessionmaker).
- `scoped_session`: according to sqlalchemy official documentation, `scoped_session` function is provided which produces a thread-managed registry of Session objects. It is commonly used in web applications so that a single global variable can be used to safely represent transactional sessions with sets of objects, localized to a single thread. In short, what there are trying to say is, use `scoped_session` in your application for thread safety. Because it open and close a session object for each reequest, this is safe and the recommended way of doing things. Read more [here](https://docs.sqlalchemy.org/en/20/orm/contextual.html#using-thread-local-scope-with-web-applications).
- `declarative_base`: this function is used to define classes mapped to relational database tables.
- `Database`: this calss is contructing a database connector that will help us connect and shutdown our database.

Now that you understand what is going on, let's proceed by creating a `settings.py` file to hold store our environmental variables. You do not want to expose your keys to public for anything. Copy and paste the below code to the file:

```python
# Stdlib Imports
from functools import lru_cache
from pydantic import BaseSettings

# Third Party Imports
from decouple import config as environ


class Settings(BaseSettings):
    """Settings to hold environmental variables."""

    VOYAGE_API_KEY: str = environ("VOYAGE_API_KEY", cast=str)
    VOYAGE_SECRET_KEY: str = environ("VOYAGE_SECRET_KEY", cast=str)


@lru_cache
def get_setting_values() -> Settings:
    env_var = Settings()
    return env_var
```

Let's go over what is going on in our code:

- `lru_cache`: this decorator will create the `Settings` object once, that is, the first time it was called. After that, it will be cached and be reused, instead of having to create the `Settings` object everytime we want to access our keys.
- `BaseSettings`: allows values to be overridden by environment variables. This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose), Heroku and any 12 factor app design.

Now that we have created the Settings object responsible for getting our environment variables, we need to create a `.env` that will be loaded by `environ`. Copy and paste the below code into the file:

```bash
VOYAGE_API_KEY=value
VOYAGE_SECRET_KEY=value
```

6). Initialize `alembic` to handle database migrations

7). Create `schemas` Directory

8). Create `interface` Directory

9). Create `services` Directory

10). Create `api` Directory

Next would be to replace the `value` with the correct keys from your vonyage [dashboard](https://dashboard.nexmo.com/).

## Conclusion
