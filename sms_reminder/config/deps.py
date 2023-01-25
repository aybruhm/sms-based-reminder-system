# Own Imports
from sms_reminder.config.database import SessionLocal


def get_db_session():
    """
    This function creates a database session,
    yields it to the caller,
    and then closes the session.
    """

    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()
