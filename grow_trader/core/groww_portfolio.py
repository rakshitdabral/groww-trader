import pandas as pd
import os
import sys
from dotenv import load_dotenv
from growwapi import GrowwAPI

from grow_trader.utils.groww_utils.authentication import get_grow_access_token
from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException

load_dotenv()

class GrowwPortfolio:
    def __init__(self, groww_auth_token: str = get_grow_access_token()):
        self.groww_auth_token = groww_auth_token

    def get_portfolio(self):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            portfolio = groww.get_holdings_for_user(timeout=5)
            return portfolio
        except Exception as e:
            raise CustomException(e,sys)

    def get_position_for_user(self,segment:str=None):
        try:
            groww = GrowwAPI(self.groww_auth_token)
            if segment.upper() == "CASH":
                position = groww.get_positions_for_user(segment=groww.SEGMENT_CASH,timeout=5)
            elif segment.upper() == "FUTURES":
                position = groww.get_positions_for_user(segment=groww.SEGMENT_FNO,timeout=5)
            else:
                position = groww.get_positions_for_user()
            return position
        except Exception as e:
            raise CustomException(e,sys)