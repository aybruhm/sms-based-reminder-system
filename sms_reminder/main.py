# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI


app = FastAPI(
    title="SMS Reminder System",
    description="An SMS reminder system that allows users to text a specific number to set reminders for themselves.",
    verison=1.0
)


if __name__ == "__main__":
    uvicorn.run("sms_reminder.main:app", host="0.0.0.0", port=3030)