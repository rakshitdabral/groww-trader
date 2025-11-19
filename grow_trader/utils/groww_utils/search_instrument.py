import os
import sys
from growwapi import GrowwAPI

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException


def search_instrument(groww_symbol:str, exchange:str=None):
    try:
        API_AUTH_TOKEN = os.getenv("GROWW_ACCESS_TOKEN")
        if not API_AUTH_TOKEN:
            msg = "Environment variables 'GROWW_ACCESS_TOKEN' is  missing."
            logging.error(msg)
            raise CustomException(msg, sys)
        
        groww = GrowwAPI(API_AUTH_TOKEN)
        original_symbol = groww_symbol.upper()
        
        symbols_to_try = []
        
        if exchange:
            exchange_upper = exchange.upper()
            if exchange_upper == "NSE":
                symbols_to_try.append(f"NSE-{original_symbol}")
            elif exchange_upper == "BSE":
                symbols_to_try.append(f"BSE-{original_symbol}")
        symbols_to_try.append(original_symbol)
        
        for symbol_to_try in symbols_to_try:
            try:
                get_instrument_by_groww_symbol_response = groww.get_instrument_by_groww_symbol(
                    groww_symbol=symbol_to_try
                )
                if get_instrument_by_groww_symbol_response is not None:
                    return get_instrument_by_groww_symbol_response
            except Exception as e:
                # Log the error but continue trying other formats
                logging.debug(f"Failed to find instrument with symbol '{symbol_to_try}': {str(e)}")
                continue
        
        # If all formats failed, raise error with helpful message
        exchange_info = f" on {exchange}" if exchange else ""
        msg = f"Instrument not found for symbol '{original_symbol}'{exchange_info}. Please verify the symbol is correct and try again."
        logging.error(msg)
        raise CustomException(msg, sys)
    except CustomException:
        raise
    except Exception as e:
        raise CustomException(e, sys) from e