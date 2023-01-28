# Stdlib Imports
from typing import Dict

# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from sms_reminder.config.settings import get_setting_values as settings

# Third Party Imports
import httpx
import backoff


class VonageSMS:
    """SMS API Service provider to handle sending text messages."""

    def __init__(self) -> None:
        """
        The method is used to initialize the class
        and set the base_url, seetings, secret_key and api_key.
        """

        self.base_url = "https://rest.nexmo.com/sms/json"
        self.settings = settings()
        self.secret_key = self.settings.VOYAGE_SECRET_KEY
        self.api_key = self.settings.VOYAGE_API_KEY

    def headers(self) -> Dict[str, str]:
        """
        This method returns a header with a key of "Content-Type" and a value of
        "application/x-www-form-urlencoded".
        """

        return {"Content-Type": "application/x-www-form-urlencoded"}

    @backoff.on_exception(backoff.expo, httpx.ConnectTimeout, max_time=100)
    async def send(self, phone_number: str, message: str) -> True:
        """
        This method sends a message to a phone number using the VonageSMS API.

        :param phone_number: The phone number to send the message to
        :type phone_number: str

        :param message: The message you want to send
        :type message: str

        :return: True
        """

        async with httpx.AsyncClient() as client:
            request_data = f"from=Send Reminder!&text={message}&to={phone_number}&api_key={self.api_key}&api_secret={self.secret_key}"
            response = await client.post(
                url=self.base_url, headers=self.headers(), data=request_data
            )
            response_data = response.json()["messages"][0]

            if response_data["status"] == "0":
                return True
            raise HTTPException(
                500,
                {
                    "source": "VonageSMS",
                    "message": response_data["error-text"],
                },
            )


vonage_sms = VonageSMS()
