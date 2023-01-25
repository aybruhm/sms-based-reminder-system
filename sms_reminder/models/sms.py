# SQLAlchemy Imports
from sqlalchemy import Column, String, DateTime

# Own Imports
from sms_reminder.config.database import Base
from sms_reminder.models.base import ObjectTracker


class Reminder(ObjectTracker, Base):
    __tablename__ = "reminders"

    phone_number = Column(String)
    message = Column(String)
    remind_when = Column(DateTime)
