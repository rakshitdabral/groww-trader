from growwapi import GrowwAPI
from dotenv import load_dotenv
import os
import sys

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException

load_dotenv()


def get_user_portfolio():
    try:
        API_AUTH_TOKEN = os.getenv("GROWW_ACCESS_TOKEN")
        if not API_AUTH_TOKEN:
            msg = "Environment variables 'GROWW_ACCESS_TOKEN' is  missing."
            logging.error(msg)
            raise CustomException(msg, sys)
        try:
            groww = GrowwAPI(API_AUTH_TOKEN)
            holdings_response = groww.get_holdings_for_user(timeout=5)
        except Exception as e:
            raise CustomException(e,sys)
        logging.info("Holdings Fetched Successfully")
        return holdings_response

    except Exception as e:
        raise CustomException(e,sys)