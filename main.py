from grow_trader.utils.groww_utils.authentication import get_grow_access_token
from grow_trader.utils.groww_utils.portfolio import get_user_portfolio
from grow_trader.core.order import Order
from grow_trader.utils.groww_utils.search_instrument import search_instrument
from grow_trader.core.vector_db_search import VectorDBSearch
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        # Test VectorDBSearch
        # get_grow_access_token()
        # print(VectorDBSearch().search("IDEA"))
        # print(Order().place_order(trading_symbol="IDEA", quantity=1, price=11.0))
        # print(Order().modify_order(order_id="GLT251116205912P35THIBVY2H5", quantity=2, price=11.0))

        # print(Order().cancel_order(order_id="GLT251116205912P35THIBVY2H5"))
        print(Order().get_trades_details(order_id="GLT251116220611GV64KYXBCZP8"))
        print(Order().get_order_status(order_id="GLT251116220611GV64KYXBCZP8"))
        print(Order().get_order_list())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()