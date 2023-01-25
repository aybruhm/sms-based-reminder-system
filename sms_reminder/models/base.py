# Stdlib Imports
from datetime import datetime

# SQLAlchemy Imports
from sqlalchemy import Column, Integer, DateTime


class ObjectTracker(object):
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, onupdate=datetime.now)
