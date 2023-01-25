# Stdlib Imports
from datetime import datetime
from pydantic import BaseModel, Field


class BaseReminderSchema(BaseModel):
    phone_number: str = Field(
        description="What's your phone number? Ensure it is valid."
    )
    message: str = Field(
        description="What message do you want to remind yourself with? E.g Time to go to the gym!"
    )
    remind_when: datetime = Field(
        description="When should I send this message to you?"
    )


class CreateReminderSchema(BaseReminderSchema):
    pass


class ReminderSchema(BaseReminderSchema):
    id: int
    date_created: datetime

    class Config:
        orm_mode = True
