# Stdlib Imports
from typing import Dict

# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from sms_reminder.config.settings import get_setting_values as settings

# Third Party Imports
import httpx


class VoyageSMS:
    """SMS API Service provider to handle sending text messages."""

    def __init__(self, secret_key: str, api_key: str) -> None:
        self.base_url = "https://rest.nexmo.com/sms/json"
        self.secret_key = secret_key
        self.api_key = api_key

    def headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/x-www-form-urlencoded"}

    async def send(self, phone_number: str, message: str) -> True:
        """
        This method sends a message to a phone number using the VoyageSMS API.

        :param phone_number: The phone number to send the message to
        :type phone_number: str

        :param message: The message you want to send
        :type message: str

        :return: True
        """

        async with httpx.AsyncClient() as client:
            request_data = f"from=Send Reminder!&text={message}&to={phone_number}&api_key={self.api_key}&api_secret={self.secret_key}"
            response = await client.post(
                url=self.base_url,
                headers=self.headers(),
                data=request_data,
                timeout=2,
            )
            response_data = response.json()["messages"][0]

            if response_data["status"] == "0":
                return True
            raise HTTPException(
                500,
                {
                    "source": "voyagesms",
                    "message": response_data["error-text"],
                },
            )


voyage_sms = VoyageSMS(
    secret_key=settings().VOYAGE_SECRET_KEY,
    api_key=settings().VOYAGE_API_KEY,
)
