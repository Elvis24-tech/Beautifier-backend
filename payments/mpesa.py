import requests
import base64
from datetime import datetime
from decouple import config


def get_access_token():
    consumer_key = config("MPESA_CONSUMER_KEY")
    consumer_secret = config("MPESA_CONSUMER_SECRET")

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(consumer_key, consumer_secret))
    data = response.json()

    return data["access_token"]

def stk_push(phone, amount, account_reference, transaction_desc):
    access_token = get_access_token()

    shortcode = config("MPESA_SHORTCODE")
    passkey = config("MPESA_PASSKEY")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        (shortcode + passkey + timestamp).encode()
    ).decode()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": config("MPESA_CALLBACK_URL"),
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()