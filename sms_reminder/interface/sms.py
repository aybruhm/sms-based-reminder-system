# Stdlib Imports
from typing import List
from datetime import datetime

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from sms_reminder.models.sms import Reminder
from sms_reminder.config.database import SessionLocal


class ReminderORMInterface:
    """Reminder ORM that interface with the database."""

    def __init__(self) -> None:
        self.db: Session = self.get_db_session().__next__()

    def get_db_session(self):
        """
        This method creates a database session, 
        yields it to the caller, rollback the session 
        if an exception occurs; otherwise, close the session.
        """

        session = SessionLocal()

        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()

    async def get(self) -> List[Reminder]:
        """This method gets a list of reminders."""

        reminders = self.db.query(Reminder).all()
        return reminders

    async def create(
        self, phone_number: str, message: str, remind_when: datetime
    ) -> Reminder:
        """This method creates a new reminder to the database."""

        reminder = Reminder(
            phone_number=phone_number,
            message=message,
            remind_when=remind_when,
        )

        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)

        return reminder


reminder_orm = ReminderORMInterface()
