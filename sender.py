import requests
from requests.models import HTTPError

class SMS_Sender():
    def __init__(self, token):
        super().__init__()
        self.BASE_URI = "https://gatewayapi.com/rest/mtsms"
        self.token = token

    def send(self, sender, message, recipient_number, send_at):
        payload = {
            "sender": sender,
            "message": message,
            "recipients": [
                {"msisdn": recipient_number}
            ],
            "sendtime": send_at
        }
        print(payload)
        resp = requests.post(
            "https://gatewayapi.com/rest/mtsms",
            json=payload,
            auth=(self.token, ""),
        )
        resp.raise_for_status()

        return resp.json()

