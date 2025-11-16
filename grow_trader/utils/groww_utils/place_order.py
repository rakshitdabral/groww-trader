from growwapi import GrowwAPI
import os
import sys
from dotenv import load_dotenv

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException
from grow_trader.utils.groww_utils import search_instrument

load_dotenv()

def place_order(trading_symbol:str):
    try:
        API_AUTH_TOKEN = os.getenv("GROWW_ACCESS_TOKEN")
        if not API_AUTH_TOKEN:
            msg = "Environment variables 'GROWW_ACCESS_TOKEN' is  missing."
            logging.error(msg)
            raise CustomException(msg, sys)
        
        groww = GrowwAPI(API_AUTH_TOKEN)
        place_order_response = groww.place_order(
            trading_symbol=trading_symbol,
            quantity=1, 
            validity=groww.VALIDITY_DAY,
            exchange=groww.EXCHANGE_NSE,
            segment=groww.SEGMENT_CASH,
            product=groww.PRODUCT_CNC,
            order_type=groww.ORDER_TYPE_LIMIT,
            transaction_type=groww.TRANSACTION_TYPE_BUY,
            price=250,               # Optional: Price of the stock (for Limit orders)
            trigger_price=245,       # Optional: Trigger price (if applicable)
            order_reference_id="Al-654321234-1628190"  # Optional: User provided 8 to 20 length alphanumeric reference ID to track the order
        )
        return place_order_response
    except Exception as e:
        raise CustomException(e,sys)