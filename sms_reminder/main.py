# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI

# Own Imports
from sms_reminder.config.database import db_connect


app = FastAPI(
    title="SMS Reminder System",
    description="An SMS reminder system that allows users to text a specific number to set reminders for themselves.",
    verison=1.0,
)


@app.on_event("startup")
async def startup():
    await db_connect.connect()


@app.on_event("shutdown")
async def disconnect():
    await db_connect.disconnect()


if __name__ == "__main__":
    uvicorn.run("sms_reminder.main:app", host="0.0.0.0", port=3030)
