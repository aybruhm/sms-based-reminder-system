# Stdlib Imports
from random import randint
from datetime import datetime

# APScheduler Imports
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Own Imports
from sms_reminder.services.vonage import vonage_sms


# initialize ayncio scheduler
scheduler = AsyncIOScheduler()


async def create_reminder_job(
    phone_number: str, message: str, remind_when: datetime
) -> dict:
    """
    This function creates a job that will send a message to the provided 
    phone number at a specific time.

    :param phone_number: The phone number to send the message to
    :type phone_number: str

    :param message: The message to be sent
    :type message: str

    :param remind_when: The datetime object that represents the time when the reminder should be sent
    :type remind_when: datetime

    :return: A dictionary with the keys "scheduled" and "job_id".
    """

    job_uid = randint(0, 9999)

    reminder_job = scheduler.add_job(
        func=vonage_sms.send,
        trigger="date",
        args=(phone_number, message),
        name=f"reminder_set_{phone_number}_{job_uid}",
        id=f"{phone_number}_{job_uid}",
        next_run_time=remind_when,
    )
    return {"scheduled": True, "job_id": reminder_job.id}
