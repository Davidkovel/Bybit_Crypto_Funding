import requests
import time
import hashlib
import hmac
import json

class ApiRequest:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.recv_window = str(5000)
        self.url = "https://api-testnet.bybit.com"
        self.httpClient = requests.Session()

    def HTTP_Request(self, endPoint, method, payload, Info):
        time_stamp = str(int(time.time() * 10 ** 3))
        print(f"Request URL: {self.url + endPoint}, Method: {method}, Params: {payload}")
        signature = self.getSignature(payload, time_stamp)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json',
        }
        if method == "POST":
            response = self.httpClient.request(method, self.url + endPoint, headers=headers, data=payload)
        else:
            response = self.httpClient.request(method, self.url + endPoint, headers=headers, params=payload)

        print(response.text)
        print(response.headers)
        print("Status Code:", response.status_code)
        print(Info + " Elapsed Time : " + str(response.elapsed))
        try:
            json_response = response.json()
            return json_response
        except json.JSONDecodeError:
            print("JSON decoding failed. Response content:", response.text)
            return None

    def getSignature(self, payload, time_stamp):
        param_str = str(time_stamp) + self.api_key + self.recv_window + payload
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature
