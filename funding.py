import threading
import time
from http.client import responses

import requests
from kucoin.client import MarketData

from trade_exchanges.kucoin import KucoinFutures
from trade_exchanges.bybit import BybitFutures


class FundingCoinGlass:
    @staticmethod
    def get_info_funding_rate():
        url = "https://open-api-v3.coinglass.com/api/futures/fundingRate/exchange-list"

        headers = {"header": "API KEY   ", "accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()

        max_funding_rate_info = None
        max_funding_rate = -float("inf")

        for item in data.get("data", []):
            symbol = item.get("symbol")
            usdt_or_usd_margin_list = item.get("usdtOrUsdMarginList", [])
            token_margin_list = item.get("tokenMarginList", [])

            for entry in usdt_or_usd_margin_list + token_margin_list:
                exchange = entry.get("exchange")
                funding_rate = entry.get("fundingRate")

                if exchange == "Bybit" and funding_rate > max_funding_rate:
                    max_funding_rate = funding_rate
                    max_funding_rate_info = {
                        "symbol": symbol,
                        "exchange": exchange,
                        "fundingRate": funding_rate,
                        "nextFundingTime": entry.get("nextFundingTime")
                    }

        # Check if the max funding rate is greater than 0.004 (0.4%)
        if max_funding_rate_info and max_funding_rate > 0.004:
            return max_funding_rate_info

        return "No funding rate greater than 0.4% on Bybit found."

    @staticmethod
    def get_price_coin(coin_with_funding_rate):
        symbol = coin_with_funding_rate["symbol"]
        url = f"https://open-api-v3.coinglass.com/api/futures/pairs-markets?symbol={symbol}"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()
        symbol_price = data["price"]
        return symbol_price


class KucoinAPI:
    @staticmethod
    def get_price_and_calculate_qty(symbol):
        market_data = MarketData()
        responses = market_data.get_ticker(f"{symbol}-USDT")
        data = responses.json()
        if data["data"] == None:
            print("[INFO] Kucoin has't this symbol")
            return False
        else:
            price = data["price"]
            qty = KucoinAPI.calculate_for_qty(price, 1000)
            return {"price": price, "qty": qty}

    @staticmethod
    def calculate_quantity(price, amount_in_usd):
        """
        Calculates the quantity of a cryptocurrency that can be purchased for a given USD amount.
        """
        return amount_in_usd / price


class FundingProvider:
    def __init__(self):
        self.kucoin_futures = KucoinFutures()
        self.bybit_futures = BybitFutures()

        self.limit_price = None
        self.symbol = None
        self.qty = None

    def check_funding(self):
        coin_with_funding_rate = FundingCoinGlass.get_info_funding_rate()
        self.symbol = coin_with_funding_rate["symbol"]

        price_and_qty = KucoinAPI.get_price_and_calculate_qty(self.symbol)
        self.limit_price = price_and_qty["price"]
        self.qty = price_and_qty["qty"]
        if price_and_qty != False:
            self.execute()

        print(coin_with_funding_rate)

    def execute(self):
        # IF Bybit FUNDING -0,6% -> Kucoin short, Bybit long
        # IF Bybit FUNDING 0,4% -> Kucoin long, Bybit short
        time.sleep(2)
        self.symbol = "PUFFERUSDT"  # temporally
        self.qty = "1500"

        kucoin_thread = threading.Thread(target=self.kucoin_futures.create_market_order_sell(self.qty, symbol=self.symbol))
        bybit_thread = threading.Thread(target=self.bybit_futures.create_market_order_buy(self.qty, symbol=self.symbol))

        # Start threads
        kucoin_thread.start()
        bybit_thread.start()

        # Wait for threads to complete
        kucoin_thread.join()
        bybit_thread.join()

        # Sleep for 15 seconds before closing positions
        print("[INFO] Sleeping for 6 minutes before closing positions.")
        time.sleep(70) # :58 MINUTE START

        # Create threads for closing positions
        kucoin_close_thread = threading.Thread(target=self.kucoin_futures.close_market_order_sell(self.qty))
        bybit_close_thread = threading.Thread(target=self.bybit_futures.close_market_order_buy(self.qty, self.symbol))

        # Start threads for closing positions
        kucoin_close_thread.start()
        bybit_close_thread.start()

        # Wait for closing threads to complete
        kucoin_close_thread.join()
        bybit_close_thread.join()

        print("[INFO] All operations completed successfully.")

# # TASK FOR ME: NOW I SHOULD TO FIND HOW TO OPEN AND CLOSE POSITION IN KUCOIN
