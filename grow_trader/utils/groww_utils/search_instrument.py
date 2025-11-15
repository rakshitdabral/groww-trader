import os
import sys
from growwapi import GrowwAPI

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException

def search_instrument():
    try:
        API_AUTH_TOKEN = os.getenv("GROWW_ACCESS_TOKEN")
        if not API_AUTH_TOKEN:
            msg = "Environment variables 'GROWW_ACCESS_TOKEN' is  missing."
            logging.error(msg)
            raise CustomException(msg, sys)
        
        groww = GrowwAPI(API_AUTH_TOKEN)
        get_instrument_by_groww_symbol_response = groww.get_instrument_by_groww_symbol(
            groww_symbol="NSE-RELIANCE"
        )
        return get_instrument_by_groww_symbol_response
    except Exception as e:
        raise CustomException(e,sys)