import requests
from django.conf import settings

def send_sms(to, text):
    url = "https://api.messagepro.mn/send"
    headers = {
        "x-api-key": settings.MESSAGEPRO_API_KEY,
    }
    params = {
        "from": "72220111",
        "to": to,
        "text": text,
    }

    response = requests.get(url, headers=headers, params=params)
    return response.status_code == 200

def send_otp_message(to, code):
    message = f"Таны баталгаажуулах код: {code} >_> bi hiichlee sh dee"
    return send_sms(to, message)