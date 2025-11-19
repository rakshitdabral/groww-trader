import os
import sys
from growwapi import GrowwAPI
from dotenv import load_dotenv

import secrets
import string

from pinecone.openapi_support.model_utils import order_response_types

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException
from grow_trader.config.groww_config import GROWW_API_KEY, GROWW_API_SECRET
from grow_trader.utils.groww_utils.authentication import get_grow_access_token

load_dotenv()

class Order:
    def __init__(self, groww_api_key: str = GROWW_API_KEY, groww_api_secret: str = GROWW_API_SECRET):
        self.groww_api_key = groww_api_key
        self.groww_api_secret = groww_api_secret
        self.groww_auth_token = get_grow_access_token()

    def generate_order_reference_id(self):
        length = secrets.randbelow(13) + 8  
        
        characters = string.ascii_letters + string.digits
        reference_id = ''.join(secrets.choice(characters) for _ in range(length))
        
        return reference_id
    
    def place_order(self, trading_symbol: str, quantity: int, price: float, exchange: str = "NSE", segment: str = "CASH"):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            trading_symbol = trading_symbol.upper()
            if exchange.upper() == "NSE":
                exchange = groww.EXCHANGE_NSE
            elif exchange.upper() == "BSE":
                exchange = groww.EXCHANGE_BSE
            else:
                exchange = groww.EXCHANGE_NSE
            if segment.upper() == "CASH":
                segment = groww.SEGMENT_CASH
            elif segment.upper() == "FUTURES":
                segment = groww.SEGMENT_FNO
            else:
                segment = groww.SEGMENT_CASH
            

            order = groww.place_order(
                trading_symbol=trading_symbol, 
                quantity=quantity, 
                price=price,
                validity=groww.VALIDITY_DAY,
                segment=segment,
                product=groww.PRODUCT_CNC,
                exchange=groww.EXCHANGE_NSE,
                order_type=groww.ORDER_TYPE_LIMIT,
                transaction_type=groww.TRANSACTION_TYPE_BUY,
                trigger_price=None, # TODO: Add trigger price
                order_reference_id=self.generate_order_reference_id())
            return order
        except Exception as e:
            raise CustomException(e,sys)

    def modify_order(self, order_id: str, quantity: int, price: float):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            order = groww.modify_order(
                groww_order_id=order_id,
                quantity=quantity,
                price=price,
                segment=groww.SEGMENT_CASH,
                order_type= groww.ORDER_TYPE_LIMIT)
            return order
        except Exception as e:
            raise CustomException(e,sys)
    
    def cancel_order(self, order_id: str):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            order = groww.cancel_order(
                groww_order_id=order_id,
                segment=groww.SEGMENT_CASH,
               )
            return order
        except Exception as e:
            raise CustomException(e,sys)

    def get_trades_details(self, order_id: str):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            trades = groww.get_trade_list_for_order(
                groww_order_id=order_id,
                segment=groww.SEGMENT_CASH,
                page=0,
                page_size=10,
            )
            return trades
        except Exception as e:
            raise CustomException(e,sys)

    def get_order_status(self, order_id: str):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            order_status = groww.get_order_status(
                groww_order_id=order_id,
                segment=groww.SEGMENT_CASH,
            )
            return order_status
        except Exception as e:
            raise CustomException(e,sys)

    def get_order_by_reference_id(self, reference_id: str):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            order = groww.get_order_status_by_reference(
                order_reference_id=reference_id,
                segment=groww.SEGMENT_CASH,
            )
            return order
        except Exception as e:
            raise CustomException(e,sys)

    def get_order_list(self):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            order_list = groww.get_order_list(
                segment=groww.SEGMENT_CASH,
                page=0,
                page_size=10,
            )
            return order_list
        except Exception as e:
            raise CustomException(e,sys)

    def get_order_details(self, order_id: str):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            order_details = groww.get_order_detail(
                groww_order_id=order_id,
                segment=groww.SEGMENT_CASH,
            )
            return order_details
        except Exception as e:
            raise CustomException(e,sys)