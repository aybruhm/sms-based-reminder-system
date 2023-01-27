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

FastAPI is a modern, fast (high-performance), a web framework for building APIs with Python 3.6+ based on standard Python type hints. It is built on top of Starlette for the web parts and Pydantic for the data parts. Its advantages are the ability to create endpoints quickly, having built-in support for WebSockets and being asynchronous. I would use Python for the backend system because of its simplicity and scalability as well as its vast ecosystem and libraries that can be used for a wide range of tasks.

> Disclaimer: I would recommend you go through the FastAPI official [documentation](https://fastapi.tiangolo.com/tutorial/) or a video [tutorial](https://www.youtube.com/watch?v=7t2alSnE2-I&t=7s) to get started with the framework; as doing this would help speed things up.

Vonage's SMS API enables you to send and receive text messages to and from users worldwide, using our REST APIs. Get started [here](https://developer.vonage.com/en/messaging/sms/overview#getting-started).

- Programmatically send and receive high volumes of SMS globally.
- Send SMS with low latency and high delivery rates.
- Receive SMS using local numbers.
- Scale your applications with familiar web technologies.
- Pay only for what you use, nothing more.
- Auto-redact feature to protect privacy.

## Vonange Account Setup

To follow along with this tutorial, I would strongly advise that you set up a Vonage account. You can start by signing up [here](https://developer.vonage.com/sign-up) and start building with free credit. Once you have, kindly grab your API and Secret key at the top of the Vonage api [dashboard](https://dashboard.nexmo.com/).

## Project Setup and Installation

1). Create and Activate The Virtual Environment

To begin, start by creating a directory, a virtual environment (preferably pipenv) and activate it:

```bash
mkdir sms_reminder && cd sms_reminder
python3.9 -m pipenv shell
```

2). Install Required Dependencies

Create a `requirements.txt` file in the directory and continue by copying and pasting the code snippet below in your `requirements.txt` file:

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

Proceed to install the required packages at once using the command below:

```bash
pipenv install -r requirements.txt
```

3). Create a `main` Module

Now that you have installed the required dependencies, let's proceed by creating a `main.py` file and pasting the below code into it. This is the entry point of the backend system that will be responsible for constructing the FastAPI application, registering API routers, events to connect and disconnect the database, starting job schedulers and running the application.

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
    pass # disconnect from the database will come here


if __name__ == "__main__":
    uvicorn.run(
        "sms_reminder.main:app", host="0.0.0.0", port=3030, reload=True
    )
```

4). Create `models` Directory

We created `main.py`, the entry point of our application. Next would be creating the models' directory, and basically, what will be there is going to be our database tables defined as class(es). Let's begin, create an `__init__.py` file to inform Python to treat this directory as a module.

> I like to keep my codes clean because it helps other team members of mine to understand and tell what is going on, and to quickly start contributing or making a fix.

Let's start by creating a `base.py` file, this fill will contain a class named `ObjectTracker`. This class is a base class for all the objects that will be tracked in the database.

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

Next would be creating a `sms.py` file, copy and paste the below code into it:

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

The `Reminder` class is going to be a representation of the `reminders` table in our database. But for us to convert this object into a class that would be translated into a database table we need to configure our database.

5). Create a `config` Directory

Remember that we need to tell Python to treat this directory as a module, so we begin by creating an `__init__.py` file. Next would be creating a `database.py` file, which will hold information about configuring the database, and engine, constructing a session maker, a database connector (to connect and shutdown our database) and creating a declarative base class that would help convert our models into database table.

Let's proceed; continue by copying the below code and paste it into the `database.py` file:

```python
# SQLAlchemy Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Third Imports
from databases import Database


# create a database and engine
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

# Construct a db connector to connect, and shutdown the database
db_connect = Database(DATABASE_URL)
```

You must be thinking "Woah, things are getting pretty complex already"? Don't worry about it, I'll explain to you the magic you are seeing.

- `create_engine`: Basically, this method is taking in the connection (database) URL and returns a sqlalchemy engine that references both a Dialect and a Pool, which together interpret the DBAPI's module functions as well as the behaviour of the database ([Source](https://www.geeksforgeeks.org/connecting-to-sql-database-using-sqlalchemy-in-python/#:~:text=The%20create_engine()%20method%20of,the%20behavior%20of%20the%20database.)).
- `session_maker`: to explain this, we need to start by understanding what a `Session` is. A Session in sqlalchemy establishes all conversations with the database, it is a regular python class which can directly be instantiated. The `session_maker` is used to create a top-level `Session` configuration which can then be used throughout an application without the need to repeat certain configurational arguments. Read more [here](https://www.geeksforgeeks.org/sqlalchemy-orm-creating-session/) and [here](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-make-a-sessionmaker).
- `scoped_session`: according to sqlalchemy official documentation, the `scoped_session` function is provided which produces a thread-managed registry of Session objects. It is commonly used in web applications so that a single global variable can be used to safely represent transactional sessions with sets of objects, localized to a single thread. In short, what there are trying to say is, to use `scoped_session` in your application for thread safety. Because it opens and closes a session object for each request, this is a safe and recommended way of doing things. Read more [here](https://docs.sqlalchemy.org/en/20/orm/contextual.html#using-thread-local-scope-with-web-applications).
- `declarative_base`: this function is used to define classes mapped to relational database tables.
- `Database`: this class is constructing a database connector that will help us connect and shut down our database.

Now that you understand what is going on, let's proceed by adding `Base` to the `Reminder` class in `sms` models:

```python
# SQLAlchemy Imports
from sqlalchemy import Column, String, DateTime

# Own Imports
from sms_reminder.config.database import Base # new line
from sms_reminder.models.base import ObjectTracker


class Reminder(ObjectTracker, Base): # added Base
    __tablename__ = "reminders" # new line

    phone_number = Column(String)
    message = Column(String)
    remind_when = Column(DateTime)
```

Doing the above will help tell sqlalchemy to map the defined class to a relational database table. Next would be updating the `main.py` entry point to connect and shutdown our database whenever our backend server emits a `startup` and `shutdown` event:

```python
# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI

# Own Imports
from sms_reminder.config.database import db_connect # new line


# construct application
app = FastAPI(
    title="SMS Reminder System",
    description="An SMS reminder system that allows users to text a specific number to set reminders for themselves.",
    verison=1.0,
)


@app.on_event("startup")
async def startup():
    scheduler.start()
    await db_connect.connect() # new line


@app.on_event("shutdown")
async def disconnect():
    await db_connect.disconnect() # new line


if __name__ == "__main__":
    uvicorn.run(
        "sms_reminder.main:app", host="0.0.0.0", port=3030, reload=True
    )

```

Now that we have updated our models and server entry point, let's proceed by creating a `settings.py` file to hold and store our environmental variables. You do not want to expose your keys to the public for anything. Copy and paste the below code to the file:

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

Let's go over what we have done:

- `lru_cache`: this decorator will create the `Settings` object once. After that, it will be cached and reused, instead of having to create the `Settings` object every time we want to access the values.
- `BaseSettings`: allows values to be overridden by environment variables. This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose), Heroku and any 12-factor app design.

Now that we have created the Settings object responsible for getting our environment variables, we need to create a `.env` that will be loaded by `environ`. Copy and paste the below code into the file:

```bash
VOYAGE_API_KEY=value
VOYAGE_SECRET_KEY=value
```

Next would be to replace the `value` with the correct keys from your Vonage [dashboard](https://dashboard.nexmo.com/).

6). Initialize `alembic` to handle database migrations

Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. It is widely used for database migrations. Let's proceed to use it.

We have had it installed from the start of our project, so what we need to do now is initialize alembic to our working project directory. Run the below command in your terminal:

```bash
alembic init migrations
```

I used `migrations` because I want that everything database migrations to be stored in that folder. Running the above command will create a folder named `migrations` with the following files/folder in it:

```bash
- env.py
- README
- script.py.mako
- versions (folder)
```

In the project directory, a file `alembic.ini` will also be created. There will be no version files in your `versions` directory because we haven’t made any migrations yet. Now to use alembic we need to do certain changes in these files. First, change the `sqlalchemy.url` in your `alembic.ini` file:

```bash
sqlalchemy.url = sqlite:///./sms_reminder.sqlite
```

Next would be to give our database model to alembic and access the metadata from the model. Edit your `env.py` file inside your `migrations` folder:

```python
... # this means there are other imports here

# Own Imports
from sms_reminder.models.sms import Reminder # new line

... # this means there are other codes above
target_metadata = Reminder.metadata # update
```

As shown above, we have to give the model base file to alembic. Now we are all set for our first migration. Run the below command on your terminal:

```bash
alembic revision --autogenerate -m "Create reminder table"
```

Running the above command will tell alembic to generate our migration file in the `versions` folder. Once this file is generated, we are ready for database migration. Run the below command:

```bash
alembic upgrade head
```

Once you run the above command, your tables will be generated in your database. That's all to the magic. Read more about alembic [here](https://alembic.sqlalchemy.org/en/latest/).

7). Create `schemas` Directory

We successfully created our `models` classes that are represented to database table(s), and made database migrations. Next would be creating our pydantic models. Pydantic is basically used for data parsing and validation using type annotation. An interesting thing to note is, _pydantic forces type hints at runtime, and provides user friendly errors when data is invalid._ To begin, create an `__init__.py` file to tell Python to treat the directory as a module, create another file named `crud.py` and paste the below codes inside it:

```python
# Stdlib Imports
import pytz
from datetime import datetime
from pydantic import BaseModel, Field


class BaseReminderSchema(BaseModel):
    phone_number: str = Field(
        description="What's your phone number? Ensure you include your country code and is valid. E.g 234xxxxxxxxxx"
    )
    message: str = Field(
        description="What message do you want to remind yourself with? E.g Time to go to the gym!"
    )
    remind_when: datetime = Field(
        description="When should I send this message to you?",
        default=datetime.now(tz=pytz.timezone("Africa/Lagos")),
    )
    

class CreateReminderSchema(BaseReminderSchema):
    pass


class ReminderSchema(BaseReminderSchema):
    id: int
    date_created: datetime

    class Config:
        orm_mode = True
```

Let's go over what's happening in the above code. We are importing the python timezone (`pytz`) library, datetime from the `datetime` library and importing BaseModel and Field from `pydantic`.

- `pytz`: this library allows accurate and cross platform timezone calculations using Python 2.4 or higher. It also solves the issue of ambiguous times at the end of daylight saving time. Read more [here](https://pythonhosted.org/pytz/).
- `BaseModel`: this is a class used in defining objects in pydantic. You can think of models as similar to types in strictly typed languages, or as the requirements of a single endpoint in an API. Read more [here](https://docs.pydantic.dev/usage/models/).
- `Field`: this is a class used to provide extra information about a field, either for the model schema or complex validation.
- `BaseReminderSchema`: this is a class that inherits from `BaseModel` to create fields that will be used across others schemas.
- `CreateReminderSchema`: this is a class that inherits from `BaseReminderSchema` that will be used as a requirement to create a reminder.
- `ReminderSchema`: this is a class that inherits from `BaseReminderSchema` that will be used as a requirement to list reminders created. The `orm_mode` (aka arbitrary class instances) support models that map to ORM objects.

8). Create `interface` Directory

9). Create `services` Directory

10). Create `api` Directory

## Conclusion

If you got here, I am proud of you. You learnt in this article how to build an SMS reminder backend system using FastAPI and Vonage SMS API. You can do so much more like throttling the `create-reminder` API to handle 10/minute to reduce spam bots.

You can reach out to me on [LinkedIn](https://linkedin.com/in/abraham-israel). Also, find the source code for this tutorial project on my [Github](https://github.com/aybruhm/sms-based-reminder-system).
