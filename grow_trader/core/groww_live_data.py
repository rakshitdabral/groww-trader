import os
import sys
from dotenv import load_dotenv
from growwapi import GrowwAPI

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException
from grow_trader.utils.groww_utils.authentication import get_grow_access_token

class GrowwLiveData:
    def __init__(self, groww_auth_token: str = get_grow_access_token()):
        self.groww_auth_token = groww_auth_token
    
    def get_live_quote(self,trading_symbol:str, exchange:str=None, segment:str=None):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            trading_symbol = trading_symbol.upper()
            if exchange.upper() == "NSE":
                exchange = groww.EXCHANGE_NSE
            elif exchange.upper() == "BSE":
                exchange = groww.EXCHANGE_BSE
            else:
                exchange = None
            if segment.upper() == "CASH":
                segment = groww.SEGMENT_CASH
            elif segment.upper() == "FUTURES":
                segment = groww.SEGMENT_FNO
            else:
                segment = None
            live_quote = groww.get_quote(trading_symbol=trading_symbol, exchange=exchange, segment=segment,timeout=5)
            return live_quote
        except Exception as e:
            raise CustomException(e,sys)

    def get_ltp(self,trading_symbol:str, segment:str=None , exchange:str=None):
        """
        This function is used to get the LTP of a trading symbol
        Args:
            trading_symbol: The trading symbol of the stock
            segment: The segment of the stock
            exchange: The exchange of the stock
        Returns:
            ltp: The LTP of the stock

        I am going to use exchange parameter to actually join the exchange with the trading symbol to get 
        the correct symbol to get the LTP.
        """
        try:
            groww = GrowwAPI(self.groww_auth_token)
            trading_symbol = trading_symbol.upper()
            if exchange.upper() == "NSE":
                symbol = f"NSE_{trading_symbol}"
            elif exchange.upper() == "BSE":
                symbol = f"BSE_{trading_symbol}"
            else:
                symbol = trading_symbol
            if segment.upper() == "CASH":
                segment = groww.SEGMENT_CASH
            elif segment.upper() == "FUTURES":
                segment = groww.SEGMENT_FNO
            else:
                segment = None
            ltp = groww.get_ltp(exchange_trading_symbols=symbol, segment=segment,timeout=5)
            return ltp
        except Exception as e:
            raise CustomException(e,sys)