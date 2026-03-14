import requests

base_url = "https://testnet.binancefuture.com"

response = requests.get(f"{base_url}/fapi/v1/time")

print("Status:", response.status_code)
print("Response:", response.text)