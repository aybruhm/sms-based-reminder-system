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
SessionLocal = scoped_session(session_factory)


# Construct a base class for declarative class definitions
Base = declarative_base()

# Construct a db connector to connect, shutdown database
db_connect = Database(DATABASE_URL)
