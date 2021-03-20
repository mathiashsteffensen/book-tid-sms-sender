import json
import arrow
import os
import requests

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

def lambda_handler(event, context):
        API_CREDENTIALS = json.loads(os.getenv("GATEWAY_API_CREDENTIALS"))

        body = json.loads(event["body"])

        print(body, type(body))

        sender = SMS_Sender(API_CREDENTIALS["token"])

        receiver_name = body["receiver"]["name"]
        business_name = body["businessName"]
        service = body["service"]
        time_of_appointment = arrow.get(int(body["appointmentAt"])).format("DD. MMMM kl. HH:mm", locale="da")

        msg = f"""Kære {receiver_name}

Vi vil minde dig om at du har booket en tid til {service} {time_of_appointment}

Venlig Hilsen
{business_name}"""

        text_info = sender.send(body["sendAs"], msg, body["receiver"]["number"], body["sendAt"])

        print(text_info["usage"]["total_cost"])

        return text_info["usage"]["total_cost"]
