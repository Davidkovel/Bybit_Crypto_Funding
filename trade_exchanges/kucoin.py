from kucoin_futures.client import Trade
from config import kucoin_api_key, kucoin_secret_key, kucoin_api_passphrase


class KucoinFutures:
    def __init__(self):
        self.client = Trade(key=kucoin_api_key, secret=kucoin_secret_key, passphrase=kucoin_api_passphrase)
        self.order_id = None

    def create_market_order_sell(self, size, symbol="XBTUSDTM"):
        self.order_id = self.client.create_market_order('PUFFERUSDTM', 'buy', "10", qty=size)

    def close_market_order_sell(self, size):
        self.order_id = self.client.create_market_order('PUFFERUSDTM', 'sell', "10", qty=size)
