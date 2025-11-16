import os, requests
from dotenv import load_dotenv

load_dotenv()

EVERSEND_CLIENT_ID = os.getenv("EVERSEND_CLIENT_ID")
EVERSEND_CLIENT_SECRET = os.getenv("EVERSEND_CLIENT_SECRET")
EVERSEND_BASE_URL = os.getenv("EVERSEND_API_BASE", "https://api.eversend.co/v1")

def get_access_token():
    url = f"{EVERSEND_BASE_URL}/auth/token"
    payload = {"client_id": EVERSEND_CLIENT_ID, "client_secret": EVERSEND_CLIENT_SECRET}
    res = requests.post(url, json=payload)
    res.raise_for_status()
    return res.json()["access_token"]

def initiate_mobile_money(amount, currency, phone_number, method, callback_url):
    token = get_access_token()
    url = f"{EVERSEND_BASE_URL}/collections/mobile-money"
    payload = {
        "amount": amount,
        "currency": currency,
        "phone_number": phone_number,
        "network": method,
        "callback_url": callback_url,
        "reason": "Edumentor subscription payment"
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers)
    res.raise_for_status()
    return res.json()
