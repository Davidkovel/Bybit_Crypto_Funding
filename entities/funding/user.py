import json
import uuid
import time
from abc import ABC, abstractmethod

from infrastructure.api import http_request


class UserAccount(ABC):
    def __init__(self, symbol="None"):
        self.symbol = symbol

    # @property
    # def symbol(self):
    #     return self.symbol
    #
    # @symbol.setter
    # def symbol(self, symbol):
    #     self.symbol = symbol


symbol = "CARVUSDT"
user_account_obj = UserAccount(symbol)
