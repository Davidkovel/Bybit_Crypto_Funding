from entities.funding.user import *


class SpotTrading(UserAccount):
    def __init__(self):
        pass

    def create_order_spot(self, side, qty, order_type="Market", time_in_force="GTC"):
        endpoint = "/v5/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        self.qty = qty
        params = json.dumps({
            "category": "spot",
            "symbol": user_account_obj.symbol,
            "side": side,
            "orderType": order_type,
            "qty": qty,
            "timeInForce": time_in_force,
            "orderLinkId": orderLinkId
        })
        http_request(endpoint, method, params, "Create Order Spot")

    def close_order_spot(self):
        endpoint_balance = "/v5/asset/transfer/query-account-coin-balance"
        method_balance = "GET"
        params = f'accountType=UNIFIED&coin=BTC'
        balance_response = http_request(endpoint_balance, method_balance, params, "Get Balance")

        current_balance = round(float(balance_response['result']['balance']['transferBalance']), 4)
        print(current_balance)

        endpoint_order = "/v5/order/create"
        method_order = "POST"
        orderLinkId = uuid.uuid4().hex

        params_order = json.dumps({
            "category": "spot",
            "symbol": user_account_obj.symbol,
            "side": "Sell",
            "orderType": "Market",
            "qty": str(current_balance),
            "timeInForce": "GMT",
            "orderLinkId": orderLinkId
        })

        # Execute the sell order
        http_request(endpoint_order, method_order, params_order, "Create Order Spot To Sell All")
