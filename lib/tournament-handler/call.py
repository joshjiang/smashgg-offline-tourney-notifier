# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)


def call(message):
    try:
        call = client.calls.create(
            twiml=f'<Response><Say>A new tournament near you added on smash.gg: {message}</Say></Response>',
            to='+18287354503',
            from_='+14044767610',
        )

        print(call.sid)
    except Exception as e:
        print(e)
        return(e)
