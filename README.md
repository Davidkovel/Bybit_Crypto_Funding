# Bybit_Crypto_Funding

## Example api request with security parameters:
```python
import hmac
import requests
import time

api_key = "XXXX"
secret_key = "XXXX"
httpClient = requests.Session()
recv_window = str(5000)
url = "https://api-testnet.bybit.com"  # Testnet endpoint


def HTTP_Request(endPoint, method, payload, Info):
    global time_stamp
    time_stamp = str(int(time.time() * 10 ** 3))
    signature = genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if (method == "POST"):
        response = httpClient.request(method, url + endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url + endPoint + "?" + payload, headers=headers)
    print(response.text)
    print(response.headers)
    print(Info + " Elapsed Time : " + str(response.elapsed))


def genSignature(payload):
    param_str = str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    return signature

# Cancel Order
endpoint = "/v5/order/cancel"
method = "POST"
params = '{"category":"linear","symbol": "BTCUSDT","orderLinkId": "' + orderLinkId + '"}'
HTTP_Request(endpoint, method, params, "Cancel")
```