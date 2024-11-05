import requests
import time
import hmac
import hashlib
import json

from config import api_key, secret_key
# Base URL for Bybit API
BASE_URL = "https://api.bytick.com"
RECV_WINDOW = str(5000)


# Function to generate signature
def get_signature(api_key, secret_key, payload, timestamp):
    param_str = str(timestamp) + api_key + RECV_WINDOW + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    return hash.hexdigest()


# Function to make the HTTP request
def http_request(endpoint, method, payload, info):
    timestamp = str(int(time.time() * 10 ** 3))
    print(f"Request URL: {BASE_URL + endpoint}, Method: {method}, Params: {payload}")

    # Get the signature for the request
    signature = get_signature(api_key, secret_key, payload, timestamp)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-RECV-WINDOW': RECV_WINDOW,
        'Content-Type': 'application/json',
    }

    # Send the request
    if method == "POST":
        response = requests.request(method, BASE_URL + endpoint, headers=headers, data=payload)
    else:
        response = requests.request(method, BASE_URL + endpoint, headers=headers, params=payload)

    print(response.text)
    print("Status Code:", response.status_code)
    print(f"{info} Elapsed Time: {response.elapsed}")

    # Attempt to parse the JSON response
    try:
        json_response = response.json()
        return json_response
    except json.JSONDecodeError:
        print("JSON decoding failed. Response content:", response.text)
        return None