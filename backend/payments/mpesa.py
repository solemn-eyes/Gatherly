import requests
from django.conf import settings

def get_access_token():

    response = requests.get(
        settings.MPESA_AUTH_URL,
        auth=(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET
        )
    )

    return response.json()["access_token"]

def stk_push(phone, amount):

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "BusinessShortCode":
            settings.MPESA_SHORTCODE,
        "Amount": amount,
        "PhoneNumber": phone,
        "CallBackURL":
            settings.MPESA_CALLBACK_URL
    }

    return requests.post(
        settings.MPESA_STK_URL,
        json=payload,
        headers=headers
    )
