# FastAPI Imports
from fastapi import APIRouter, status

# Own Imports
from sms_reminder.services.sms import create_user_reminder
from sms_reminder.schemas.crud import CreateReminderSchema, ReminderSchema


router = APIRouter(tags=["Reminder"])


@router.post("/create-reminder/", status_code=status.HTTP_201_CREATED)
async def create_reminder(payload: CreateReminderSchema):
    """
    This API view creates and set a reminder.

    :param payload: CreateReminderSchema\n
    :type payload: CreateReminderSchema

    :return: A dictionary with a message and a data.
    """

    reminder = create_user_reminder(
        payload.phone_number, payload.message, payload.remind_when
    )
    return {"message": "Reminder set!", "data": reminder}
