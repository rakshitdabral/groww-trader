from grow_trader.utils.groww_utils.authentication import get_grow_access_token
from grow_trader.core.groww_portfolio import GrowwPortfolio
from grow_trader.core.order import Order
from grow_trader.utils.groww_utils.search_instrument import search_instrument
from grow_trader.core.vector_db_search import VectorDBSearch
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

def format_response(response, title="Response", key_columns=None):
    """
    Generic formatter that displays any response in tabular form.
    
    Args:
        response: The response data (dict, list, or any other type)
        title: Title to display for the response
        key_columns: Optional list of column names to prioritize/display
    """
    print(f"\n{title}:")
    print("=" * 120)
    
    # Handle dictionary responses
    if isinstance(response, dict):
        # Check if it contains a list (like 'trade_list', 'order_list')
        list_keys = [key for key, value in response.items() 
                     if isinstance(value, list) and len(value) > 0]
        
        if list_keys:
            # If multiple list keys, display each
            for list_key in list_keys:
                df = pd.DataFrame(response[list_key])
                
                # Apply key_columns filter if provided
                if key_columns:
                    available_columns = [col for col in key_columns if col in df.columns]
                    if available_columns:
                        df_display = df[available_columns]
                    else:
                        df_display = df
                else:
                    df_display = df
                
                print(f"\n{list_key.replace('_', ' ').title()}:")
                print(df_display.to_string(index=False))
                print(f"\nTotal {list_key.replace('_', ' ')}: {len(df)}")
            
            # Display other non-list fields if any
            other_fields = {k: v for k, v in response.items() 
                          if k not in list_keys and not isinstance(v, (list, dict))}
            if other_fields:
                print("\nOther Fields:")
                for key, value in other_fields.items():
                    print(f"  {key}: {value}")
        
        else:
            # Single dictionary - convert to DataFrame with one row
            df = pd.DataFrame([response])
            
            # Apply key_columns filter if provided
            if key_columns:
                available_columns = [col for col in key_columns if col in df.columns]
                if available_columns:
                    df_display = df[available_columns]
                else:
                    df_display = df
            else:
                df_display = df
            
            print(df_display.to_string(index=False))
    
    # Handle list responses
    elif isinstance(response, list):
        if response:
            df = pd.DataFrame(response)
            
            # Apply key_columns filter if provided
            if key_columns:
                available_columns = [col for col in key_columns if col in df.columns]
                if available_columns:
                    df_display = df[available_columns]
                else:
                    df_display = df
            else:
                df_display = df
            
            print(df_display.to_string(index=False))
            print(f"\nTotal Items: {len(df)}")
        else:
            print("No data found")
    
    # Handle other types - fallback to JSON
    else:
        print(json.dumps(response, indent=2))
    
    print("=" * 120)

def main():
    try:
        # Test VectorDBSearch
        # get_grow_access_token()
        # print(VectorDBSearch().search("IDEA"))
        # print(Order().place_order(trading_symbol="IDEA", quantity=1, price=11.0))
        # print(Order().modify_order(order_id="GLT251116205912P35THIBVY2H5", quantity=2, price=11.0))

        # print(Order().cancel_order(order_id="GLT251116205912P35THIBVY2H5"))
        
        # order_id = "GLT251116220611GV64KYXBCZP8"
        # order = Order()
        
        # # Define key columns for better readability (optional - can be None to show all columns)
        # order_key_columns = ['groww_order_id', 'trading_symbol', 'order_status', 'quantity', 
        #                     'price', 'transaction_type', 'order_type', 'created_at']
        
        # # Format all responses using the generic formatter
        # format_response(
        #     order.get_trades_details(order_id=order_id),
        #     title="📊 Trade Details"
        # )
        
        # format_response(
        #     order.get_order_status(order_id=order_id),
        #     title="📋 Order Status",
        #     key_columns=order_key_columns
        # )
        
        # format_response(
        #     order.get_order_list(),
        #     title="📋 Order List",
        #     key_columns=order_key_columns
        # )
        
        # format_response(
        #     order.get_order_details(order_id=order_id),
        #     title="📋 Order Details",
        #     key_columns=order_key_columns
        # )

        print(GrowwPortfolio().get_position_for_user())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()