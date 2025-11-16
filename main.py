from grow_trader.utils.groww_utils.authentication import get_grow_access_token
from grow_trader.utils.groww_utils.portfolio import get_user_portfolio
from grow_trader.utils.groww_utils.place_order import place_order
from grow_trader.utils.groww_utils.search_instrument import search_instrument
from grow_trader.core.vector_db_search import VectorDBSearch
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        # Test VectorDBSearch
        get_grow_access_token()
        print(get_user_portfolio())
        print(place_order("TCS"))
        print(search_instrument())
        print(VectorDBSearch().search("HDFC"))
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()