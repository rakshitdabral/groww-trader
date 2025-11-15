from grow_trader.utils.groww_utils.authentication import get_grow_access_token
from grow_trader.utils.groww_utils.portfolio import get_user_portfolio
from grow_trader.utils.groww_utils.place_order import place_order
from grow_trader.utils.groww_utils.search_instrument import search_instrument
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        get_grow_access_token()
        print(search_instrument())

        
    except Exception as e:
        print("API Error:", e)

if __name__ == "__main__":
    main()