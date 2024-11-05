from entities.funding.user import *


class FuturesTrading(UserAccount):
    def __init__(self, buy_leverage="12", sell_leverage="12"):
        self.buy_leverage = buy_leverage
        self.sell_leverage = sell_leverage

    def set_leverage(self, category="linear"):
        endpoint = "/v5/position/set-leverage"
        method = "POST"
        params = json.dumps({
            "category": category,
            "symbol": user_account_obj.symbol,
            "buyLeverage": self.buy_leverage,
            "sellLeverage": self.sell_leverage
        })
        http_request(endpoint, method, params, "Set Leverage")

    def create_order_futures(self, side, qty, order_type="Market", time_in_force="GTC", category="linear"):
        endpoint = "/v5/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        self.qty = qty
        positionIdx = 1 if side == "Buy" else 2  # Set positionIdx based on the side for hedge mode
        params = json.dumps({
            "category": category,
            "symbol": user_account_obj.symbol,
            "side": side,
            "positionIdx": positionIdx,
            "orderType": order_type,
            "qty": qty,
            "timeInForce": time_in_force,
            "orderLinkId": orderLinkId
        })
        http_request(endpoint, method, params, f"Create Order Futures {side}")

    def create_order_futures_hedg(self, side, qty, order_type="Market", time_in_force="GTC", category="linear"):
        endpoint = "/v5/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        self.qty = qty
        params = json.dumps({
            "category": category,
            "symbol": user_account_obj.symbol,
            "side": side,
            "orderType": order_type,
            "qty": qty,
            "timeInForce": time_in_force,
            "positionIdx": 2,
            "orderLinkId": orderLinkId
        })
        http_request(endpoint, method, params, "Create Order Futures")

    def close_order_futures_hedg_short(self, side, qty, order_type="Market", time_in_force="GTC", category="linear"):
        endpoint = "/v5/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        self.qty = qty
        params = json.dumps({
            "category": category,
            "symbol": user_account_obj.symbol,
            "side": side,
            "positionIdx": 0,
            "orderType": order_type,
            "qty": qty,
            "timeInForce": time_in_force,
            "positionIdx": 0,
            "orderLinkId": orderLinkId
        })
        http_request(endpoint, method, params, "Create Order Futures")

    def change_mode(self):
        endpoint = "v5/account/set-hedging-mode"
        method = "POST"
        params = json.dumps({
            "setHedgingMode": "OFF"
        })
        http_request(endpoint, method, params, "Changing Mode to One Way")

    def close_all_positions(self, qty, category="linear"):
        # Close short position by creating a Buy order with positionIdx=2
        self.close_all_futures_orders("Buy", qty, positionIdx=2, category=category)
        time.sleep(5.2)

        # Close long position by creating a Sell order with positionIdx=1
        self.close_all_futures_orders("Sell", qty, positionIdx=1, category=category)

    def close_all_futures_orders(self, side, qty, positionIdx, order_type="Market", time_in_force="GTC",
                                 category="linear"):
        endpoint = "/v5/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        params = json.dumps({
            "category": category,
            "symbol": user_account_obj.symbol,
            "side": side,
            "positionIdx": positionIdx,
            "orderType": order_type,
            "qty": qty,
            "timeInForce": time_in_force,
            "orderLinkId": orderLinkId
        })
        http_request(endpoint, method, params, f"Create Order Futures {side} to close position")
