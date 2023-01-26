# Stdlib Imports
from typing import List
from datetime import datetime

# SQLAlchemy Imports
from sqlalchemy.orm import Session

# Own Imports
from sms_reminder.models.sms import Reminder
from sms_reminder.config.deps import get_db_session


class ReminderORMInterface:
    """Reminder ORM that interface with the database."""

    def __init__(self) -> None:
        self.orm = get_db_session()

    def get_session(self) -> Session:
        """
        This method returns the next session in the session pool.

        :return: A session object
        """

        return next(self.orm)

    async def get(self) -> List[Reminder]:
        """This method gets a list of reminders."""

        reminders = self.get_session().query(Reminder).all()
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

        # add reminder to table and commit session
        self.get_session().add(reminder)
        self.get_session().commit(reminder)
        return reminder


reminder_orm = ReminderORMInterface()
