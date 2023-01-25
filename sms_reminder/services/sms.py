# Stdlib Imports
from datetime import datetime

# Own Imports
from sms_reminder.interface.sms import reminder_orm, Reminder


async def create_user_reminder(
    phone_number: str, message: str, reminder_when: datetime
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

    reminder = await reminder_orm.create(phone_number, message, reminder_when)
    return reminder
