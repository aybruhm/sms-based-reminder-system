# FastAPI Imports
from fastapi import APIRouter

router = APIRouter(tags=["Root"])


@router.get("/")
async def root() -> dict:
    """
    SMS Reminder System root

    Returns:
        dict: version and description
    """
    return {
        "version": 1.0,
        "description": "An SMS reminder system that allows users to text a specific number to set reminders for themselves.",
    }
