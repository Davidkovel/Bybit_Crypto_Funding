import schedule
import time
from datetime import datetime, timedelta

from use_cases.funding import *

provider = FundingProvider()


def schedule_orders():
    # Schedule order placement 2 minutes before each target hour
    schedule.every().day.at("23:56").do(provider.execute)
    schedule.every().day.at("07:56").do(provider.execute)
    schedule.every().day.at("15:57").do(provider.execute)

    # Schedule order closing 2 seconds before each target hour
    schedule.every().day.at("23:59:57").do(provider.close_orders)
    schedule.every().day.at("07:59:57").do(provider.close_orders)
    schedule.every().day.at("15:59:57").do(provider.close_orders)


if __name__ == "__main__":
    # funding_obj = FundingProvider()
    # funding_obj.execute()
    schedule_orders()
    while True:
        schedule.run_pending()
        time.sleep(1)

    # Futures:
    # funding_trade_obj.set_leverage()
    # funding_trade_obj.create_order_futures("Buy", "0.002")
    # time.sleep(3)
    # funding_trade_obj.close_order_futures()

    # Spot:
    # funding_trade_obj.create_order_spot("Buy", "200")
    # time.sleep(4)
    # funding_trade_obj.close_order_spot()

# api_key = api_key
# secret_key = secret_key
# httpClient = requests.Session()
# recv_window = str(5000)
# url = "https://api-testnet.bybit.com"  # Testnet endpoint


# def HTTP_Request(endPoint, method, payload, Info):
#     global time_stamp
#     time_stamp = str(int(time.time() * 10 ** 3))
#     signature = genSignature(payload)
#     headers = {
#         'X-BAPI-API-KEY': api_key,
#         'X-BAPI-SIGN': signature,
#         'X-BAPI-SIGN-TYPE': '2',
#         'X-BAPI-TIMESTAMP': time_stamp,
#         'X-BAPI-RECV-WINDOW': recv_window,
#         'Content-Type': 'application/json'
#     }
#     if (method == "POST"):
#         response = httpClient.request(method, url + endPoint, headers=headers, data=payload)
#     else:
#         response = httpClient.request(method, url + endPoint + "?" + payload, headers=headers)
#     print(response.text)
#     print(response.headers)
#     print(Info + " Elapsed Time : " + str(response.elapsed))
#
#
# def genSignature(payload):
#     param_str = str(time_stamp) + api_key + recv_window + payload
#     hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
#     signature = hash.hexdigest()
#     return signature
#
#
# def set_leverage(symbol, buy_leverage, sell_leverage, category="linear"):
#     endpoint = "/v5/position/set-leverage"
#     method = "POST"
#     params = json.dumps({
#         "category": category,
#         "symbol": symbol,
#         "buyLeverage": buy_leverage,
#         "sellLeverage": sell_leverage
#     })
#     HTTP_Request(endpoint, method, params, "Set Leverage")
#
#
# def create_order(symbol, side, qty, order_type="Market", time_in_force="GTC", category="linear"):
#     endpoint = "/v5/order/create"
#     method = "POST"
#     orderLinkId = uuid.uuid4().hex
#     params = json.dumps({
#         "category": category,
#         "symbol": symbol,
#         "side": side,
#         "positionIdx": 0,
#         "orderType": order_type,
#         "qty": qty,
#         "timeInForce": time_in_force,
#         "orderLinkId": orderLinkId
#     })
#     HTTP_Request(endpoint, method, params, "Create Order")
#
#
# symbol = "BTCUSDT"
# buy_leverage = "5"
# sell_leverage = "5"
#
# # 1. Установить плечо
# set_leverage(symbol, buy_leverage, sell_leverage)
#
# # 2. Создать заказ
# create_order(symbol, "Buy", "0.002")

#
# # Get unfilled Orders
# endpoint = "/v5/order/realtime"
# method = "GET"
# params = 'category=linear&settleCoin=USDT'
# HTTP_Request(endpoint, method, params, "UnFilled")
#
# # Cancel Order
# endpoint = "/v5/order/cancel"
# method = "POST"
# params = '{"category":"linear","symbol": "BTCUSDT","orderLinkId": "' + orderLinkId + '"}'
# HTTP_Request(endpoint, method, params, "Cancel")
