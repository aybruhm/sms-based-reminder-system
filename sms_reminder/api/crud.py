# Stdlib Imports
from typing import List
from datetime import datetime, timezone

# FastAPI Imports
from fastapi import APIRouter, status, HTTPException

# Own Imports
from sms_reminder.services.sms import create_user_reminder, get_user_reminders
from sms_reminder.schemas.crud import CreateReminderSchema, ReminderSchema


# initialize the api router
router = APIRouter(tags=["Reminder"])


@router.post("/create-reminder/", status_code=status.HTTP_201_CREATED)
async def create_reminder(payload: CreateReminderSchema):
    """
    This API view creates and set a reminder.

    :param payload: CreateReminderSchema\n
    :type payload: CreateReminderSchema

    :return: The reminder serialized to a json.
    """

    if payload.remind_when <= datetime.now(timezone.utc):
        raise HTTPException(
            400,
            {
                "message": "Kindly set a date and time that exceeds the past and now."
            },
        )

    reminder = await create_user_reminder(
        payload.phone_number, payload.message, payload.remind_when
    )
    return {"message": "Reminder set!", "data": reminder}


@router.get("/reminders/", response_model=List[ReminderSchema])
async def get_reminders():
    """
    This API view gets the total available reminders.

    :return: A list of reminders.
    """

    reminders = await get_user_reminders()
    return reminders
