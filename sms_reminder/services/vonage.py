# Stdlib Imports
from typing import Dict

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
    
    async def send(self, to_contact: str) -> ...:
        
        async with httpx.AsyncClient() as client:
            payload = {
                "from": "Voyage Reminder",
                "text": "",
                "to": to_contact,
                "api_key": self.api_key,
                "secret_key": self.secret_key
            }
            response = await client.post(url=self.base_url, json=payload)
            print("Response: ", response.json())
            
            # if response.json()["messages"][0]["status"] == ")":
            #     return True, ...
            # return False
