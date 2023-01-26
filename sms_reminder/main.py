# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI

# Own Imports
from sms_reminder.services.tasks import scheduler
from sms_reminder.config.database import db_connect
from sms_reminder.api.index import router as root_router
from sms_reminder.api.crud import router as crud_router


# construct application
app = FastAPI(
    title="SMS Reminder System",
    description="An SMS reminder system that allows users to text a specific number to set reminders for themselves.",
    verison=1.0,
)

# include routers
app.include_router(root_router)
app.include_router(crud_router)


@app.on_event("startup")
async def startup():
    scheduler.start()
    await db_connect.connect()


@app.on_event("shutdown")
async def disconnect():
    await db_connect.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        "sms_reminder.main:app", host="0.0.0.0", port=3030, reload=True
    )
