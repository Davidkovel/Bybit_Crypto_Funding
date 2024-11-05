import time

from entities.funding.futures import *
from entities.funding.spot import *


class FundingProvider:
    def __init__(self):
        self.futures_trading_obj = FuturesTrading()
        self.spot_trading_obj = SpotTrading()

    def close_orders(self):
        self.futures_trading_obj.close_all_positions("470")

    def execute(self):
        # Futures:
        self.futures_trading_obj.set_leverage()
        # Opening a long position (Buy)
        self.futures_trading_obj.create_order_futures("Buy", "470")
        # Opening a short position (Sell)
        self.futures_trading_obj.create_order_futures("Sell", "470")

#
# class FundingTrade:
#     def __init__(self, symbol):
#         self.symbol = symbol
#         self.buy_leverage = "10"
#         self.sell_leverage = "10"
#         self.api_request_obj = ApiRequest(api_key, secret_key)
#
#         self.qty = ""
#
#     def set_leverage(self, category="linear"):
#         endpoint = "/v5/position/set-leverage"
#         method = "POST"
#         params = json.dumps({
#             "category": category,
#             "symbol": self.symbol,
#             "buyLeverage": self.buy_leverage,
#             "sellLeverage": self.sell_leverage
#         })
#         self.api_request_obj.HTTP_Request(endpoint, method, params, "Set Leverage")
#
#     def create_order_futures(self, side, qty, order_type="Market", time_in_force="GTC", category="linear"):
#         endpoint = "/v5/order/create"
#         method = "POST"
#         orderLinkId = uuid.uuid4().hex
#         self.qty = qty
#         params = json.dumps({
#             "category": category,
#             "symbol": self.symbol,
#             "side": side,
#             "positionIdx": 0,
#             "orderType": order_type,
#             "qty": qty,
#             "timeInForce": time_in_force,
#             "orderLinkId": orderLinkId
#         })
#         self.api_request_obj.HTTP_Request(endpoint, method, params, "Create Order Futures")
#
#     # self.order_id_futures = response_text['result']['orderId']
#     # self.order_link_id_futures = response_text['result']['orderLinkId']
#
#     def create_order_spot(self, side, qty, order_type="Market", time_in_force="GTC"):
#         endpoint = "/v5/order/create"
#         method = "POST"
#         orderLinkId = uuid.uuid4().hex
#         self.qty = qty
#         params = json.dumps({
#             "category": "spot",
#             "symbol": self.symbol,
#             "side": side,
#             "orderType": order_type,
#             "qty": qty,
#             "timeInForce": time_in_force,
#             "orderLinkId": orderLinkId
#         })
#         self.api_request_obj.HTTP_Request(endpoint, method, params, "Create Order Spot")
#
#     def close_order_futures(self):
#         self.create_order_futures("Sell", self.qty)
#
#     def close_order_spot(self):
#         endpoint_balance = "/v5/asset/transfer/query-account-coin-balance"
#         method_balance = "GET"
#         params = f'accountType=UNIFIED&coin=BTC'
#         balance_response = self.api_request_obj.HTTP_Request(endpoint_balance, method_balance, params,"Get Balance")
#
#         current_balance = round(float(balance_response['result']['balance']['transferBalance']), 4)
#         print(current_balance)
#         #
#         endpoint_order = "/v5/order/create"
#         method_order = "POST"
#         orderLinkId = uuid.uuid4().hex
#
#         params_order = json.dumps({
#             "category": "spot",
#             "symbol": self.symbol,
#             "side": "Sell",
#             "orderType": "Market",
#             "qty": str(current_balance),
#             "timeInForce": "GMT",
#             "orderLinkId": orderLinkId
#         })
#
#         # Execute the sell order
#         self.api_request_obj.HTTP_Request(endpoint_order, method_order, params_order, "Create Order Spot Sell All")
