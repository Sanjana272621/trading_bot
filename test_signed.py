import os
import time
import hmac
import hashlib
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
base_url = os.getenv("BINANCE_BASE_URL")

params = {
    "timestamp": int(time.time() * 1000)
}

query = urlencode(params)

signature = hmac.new(
    api_secret.encode(),
    query.encode(),
    hashlib.sha256
).hexdigest()

params["signature"] = signature

headers = {
    "X-MBX-APIKEY": api_key
}

url = f"{base_url}/fapi/v2/balance"

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.text)