from flask import Flask, request
import arrow
import os
import json
from dotenv import load_dotenv
load_dotenv(verbose=True)

from db import DB_Conn
from sender import SMS_Sender

def run():
    server = Flask(__name__)

    API_CREDENTIALS = json.loads(os.getenv("GATEWAY_API_CREDENTIALS"))
    DB_CREDENTIALS = json.loads(os.getenv("POSTGRES_CREDENTIALS"))

    sender = SMS_Sender(API_CREDENTIALS["token"])

    init_db = DB_Conn(DB_CREDENTIALS["host"], DB_CREDENTIALS["password"])
    init_db.query.execute("CREATE TABLE IF NOT EXISTS texts (sentfrom jsonb, region varchar(25), cost float, createdAt timestamp);")
    init_db.db.commit()
    init_db.query.close()
    init_db.db.close()

    @server.route('/schedule-text', methods=["POST"])
    def schedule_text():
        body = request.json

        receiver_name = body["receiver"]["name"]
        business_name = body["businessName"]
        service = body["service"]
        time_of_appointment = arrow.get(int(body["appointmentAt"])).shift(hours=1).format("DD. MMMM kl. HH:mm", locale="da")

        print(body)

        msg = f"""Kære {receiver_name}

Vi vil minde dig om at du har booket en tid til {service} {time_of_appointment}

Venlig Hilsen
{business_name}"""

        text_info = sender.send(business_name, msg, body["receiver"]["number"], body["sendAt"])

        print(text_info["usage"]["total_cost"])

        db = DB_Conn(DB_CREDENTIALS["host"], DB_CREDENTIALS["password"])

        db.query.execute("""INSERT INTO texts (
            sentfrom, 
            region, 
            cost, 
            createdAt
        ) VALUES (%s, 'da', %s, %s)""",
        (json.dumps(body["sender"]), text_info["usage"]["total_cost"], arrow.now().format('YYYY-MM-DD HH:mm:ss')))

        db.commit()
        db.close()

        return body

    return server
