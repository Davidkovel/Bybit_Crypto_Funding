import json
import uuid

from infrastructure.api import http_request


class BybitFutures():
    def __init__(self, buy_leverage="10", sell_leverage="10"):
        self.buy_leverage = buy_leverage
        self.sell_leverage = sell_leverage

        self.symbol = None
        self.orderLinkId = None

    def set_leverage(self, symbol, category="linear"):
        endpoint = "/v5/position/set-leverage"
        method = "POST"
        params = json.dumps({
            "category": category,
            "symbol": symbol,
            "buyLeverage": self.buy_leverage,
            "sellLeverage": self.sell_leverage
        })
        http_request(endpoint, method, params, "Set Leverage")

    def create_market_order_buy(self, qty, symbol='PUFFERUSDT', side="Sell", order_type="Market", time_in_force="GTC",
                                category="linear"):
        self.symbol = symbol
        endpoint = "/v5/order/create"
        method = "POST"
        self.orderLinkId = uuid.uuid4().hex
        self.qty = qty
        positionIdx = 1 if side == "Buy" else 2  # Set positionIdx based on the side for hedge mode
        params = json.dumps({
            "category": category,
            "symbol": self.symbol,
            "side": side,
            # "positionIdx": positionIdx,
            "orderType": order_type,
            "qty": qty,
            "timeInForce": time_in_force,
            "orderLinkId": self.orderLinkId
        })
        http_request(endpoint, method, params, f"Create Order Futures {side}")

    def close_market_order_buy(self, qty, symbol='PUFFERUSDT'):
        self.create_market_order_buy(qty=qty, symbol=symbol, side="Buy")

    def change_mode(self):
        endpoint = "v5/account/set-hedging-mode"
        method = "POST"
        params = json.dumps({
            "setHedgingMode": "OFF"
        })
        http_request(endpoint, method, params, "Changing Mode to One Way")
