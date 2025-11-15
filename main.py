from grow_trader.utils.authentication import get_grow_access_token
from grow_trader.utils.portfolio import get_user_portfolio
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        get_grow_access_token()
        portfolio = get_user_portfolio()
        
        print(portfolio)
        
    except Exception as e:
        print("API Error:", e)

if __name__ == "__main__":
    main()