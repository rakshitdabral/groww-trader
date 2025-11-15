import os
import sys
from dotenv import load_dotenv
from growwapi import GrowwAPI
import pyotp

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException

load_dotenv()

def get_grow_access_token():
    try:
        api_key = os.getenv("GROWW_API_KEY")
        api_secret = os.getenv("GROWW_API_SECRET")

        if not api_key or not api_secret:
            msg = "Environment variables 'GROWW_API_KEY' or 'GROWW_API_SECRET' are missing."
            logging.error(msg)
            raise CustomException(msg, sys)

        # Generate TOTP
        try:
            totp_gen = pyotp.TOTP(api_secret)
            totp = totp_gen.now()
        except Exception as e:
            logging.error(f"Failed to generate TOTP: {e}")
            raise CustomException("TOTP generation failed", sys) from e

        # Fetch access token
        try:
            access_token = GrowwAPI.get_access_token(
                api_key=api_key,
                totp=totp
            )
        except Exception as e:
            logging.error(f"Groww API token generation failed: {e}")
            raise CustomException("Failed to obtain Groww access token", sys) from e

        if not access_token:
            msg = "Groww returned an empty access token."
            logging.error(msg)
            raise CustomException(msg, sys)

        # Store token in environment runtime
        os.environ["GROWW_ACCESS_TOKEN"] = access_token
        logging.info("Groww access token generated and stored successfully.")

        return access_token

    except CustomException as ce:
        # Already logged, just re-raise
        raise ce

    except Exception as e:
        logging.exception("Unexpected error during Groww access token generation.")
        raise CustomException("Unexpected error occurred", sys) from e
