# Stdlib Imports
from datetime import datetime
from typing import List

# Own Imports
from sms_reminder.services.vonage import voyage_sms
from sms_reminder.interface.sms import reminder_orm, Reminder


async def create_user_reminder(
    phone_number: str, message: str, remind_when: datetime
) -> Reminder:
    """
    This function creates a new reminder in the database.

    :param phone_number: The phone number of the user who will receive the reminder
    :type phone_number: str

    :param message: The message that will be sent to the user
    :type message: str

    :param reminder_when: datetime
    :type reminder_when: datetime

    :return: A reminder object
    """

    reminder = await reminder_orm.create(phone_number, message, remind_when)
    # sms_sent = await voyage_sms.send(phone_number, message)

    return reminder


async def get_user_reminders() -> List[Reminder]:
    """
    This function gets the list of user reminders.

    :return: A list of reminder objects.
    """

    reminders = await reminder_orm.get()
    return reminders
