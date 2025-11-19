import sys
from grow_trader.cli.interface import CLInterface
from grow_trader.core.groww_order import Order
from grow_trader.core.groww_portfolio import GrowwPortfolio
from grow_trader.core.groww_live_data import GrowwLiveData
from grow_trader.core.vector_db_search import VectorDBSearch
from grow_trader.utils.groww_utils.search_instrument import search_instrument

class TraderCLI:
    def __init__(self):
        self.interface = CLInterface()
        self.order = Order()
        self.portfolio = GrowwPortfolio()
        self.live_data = GrowwLiveData()
        self.vector_search = VectorDBSearch()
        
    def run(self):
        """Main application loop"""
        self.interface.clear_screen()
        self.interface.print_banner()
        
        self.interface.typing_effect("Welcome to Groww Trader CLI!", delay=0.05, style="bold green")
        self.interface.typing_effect("Initializing system...", delay=0.03, style="yellow")
        
        while True:
            try:
                main_menu = [
                    "📊 Orders Management",
                    "💼 Portfolio & Positions",
                    "📈 Live Market Data",
                    "🔍 Search Instruments",
                    "🤖 AI Vector Search",
                    "❌ Exit"
                ]
                
                choice = self.interface.show_menu(main_menu, "Main Menu")
                
                if choice == "📊 Orders Management":
                    self.handle_orders_menu()
                elif choice == "💼 Portfolio & Positions":
                    self.handle_portfolio_menu()
                elif choice == "📈 Live Market Data":
                    self.handle_live_data_menu()
                elif choice == "🔍 Search Instruments":
                    self.handle_search_menu()
                elif choice == "🤖 AI Vector Search":
                    self.handle_vector_search_menu()
                elif choice == "❌ Exit":
                    self.interface.typing_effect("Thank you for using Groww Trader CLI!", delay=0.03, style="bold cyan")
                    sys.exit(0)
                    
            except KeyboardInterrupt:
                self.interface.print_info("\nExiting...")
                sys.exit(0)
            except Exception as e:
                self.interface.print_error(f"An error occurred: {str(e)}")
    
    def handle_orders_menu(self):
        """Handle orders management menu"""
        menu_options = [
            "Place Order",
            "Modify Order",
            "Cancel Order",
            "Get Order Status",
            "Get Order List",
            "Get Order Details",
            "Get Trades Details",
            "Back to Main Menu"
        ]
        
        choice = self.interface.show_menu(menu_options, "Orders Management")
        
        if choice == "Place Order":
            self.place_order()
        elif choice == "Modify Order":
            self.modify_order()
        elif choice == "Cancel Order":
            self.cancel_order()
        elif choice == "Get Order Status":
            self.get_order_status()
        elif choice == "Get Order List":
            self.get_order_list()
        elif choice == "Get Order Details":
            self.get_order_details()
        elif choice == "Get Trades Details":
            self.get_trades_details()
    
    def place_order(self):
        """Place a new order"""
        self.interface.print_info("Place a new order")
        
        symbol = self.interface.input_prompt("Enter trading symbol: ")
        quantity = int(self.interface.input_prompt("Enter quantity: "))
        price = float(self.interface.input_prompt("Enter price: "))
        
        result = self.interface.show_loading(
            "[bold cyan]Placing order...[/bold cyan]",
            self.order.place_order,
            trading_symbol=symbol,
            quantity=quantity,
            price=price
        )
        
        if result:
            self.interface.display_response(result, "Order Placed")
            self.interface.print_success("Order placed successfully!")
    
    def modify_order(self):
        """Modify an existing order"""
        order_id = self.interface.input_prompt("Enter order ID: ")
        quantity = int(self.interface.input_prompt("Enter new quantity: "))
        price = float(self.interface.input_prompt("Enter new price: "))
        
        result = self.interface.show_loading(
            "[bold cyan]Modifying order...[/bold cyan]",
            self.order.modify_order,
            order_id=order_id,
            quantity=quantity,
            price=price
        )
        
        if result:
            self.interface.display_response(result, "Order Modified")
            self.interface.print_success("Order modified successfully!")
    
    def cancel_order(self):
        """Cancel an order"""
        order_id = self.interface.input_prompt("Enter order ID: ")
        
        result = self.interface.show_loading(
            "[bold cyan]Cancelling order...[/bold cyan]",
            self.order.cancel_order,
            order_id=order_id
        )
        
        if result:
            self.interface.display_response(result, "Order Cancelled")
            self.interface.print_success("Order cancelled successfully!")
    
    def get_order_status(self):
        """Get order status"""
        order_id = self.interface.input_prompt("Enter order ID: ")
        
        result = self.interface.show_loading(
            "[bold cyan]Fetching order status...[/bold cyan]",
            self.order.get_order_status,
            order_id=order_id
        )
        
        if result:
            key_columns = ['groww_order_id', 'trading_symbol', 'order_status', 'quantity', 
                          'price', 'transaction_type', 'order_type', 'created_at']
            self.interface.display_response(result, "Order Status", key_columns)
    
    def get_order_list(self):
        """Get list of orders"""
        result = self.interface.show_loading(
            "[bold cyan]Fetching order list...[/bold cyan]",
            self.order.get_order_list
        )
        
        if result:
            key_columns = ['groww_order_id', 'trading_symbol', 'order_status', 'quantity', 
                          'price', 'transaction_type', 'order_type', 'created_at']
            self.interface.display_response(result, "Order List", key_columns)
    
    def get_order_details(self):
        """Get order details"""
        order_id = self.interface.input_prompt("Enter order ID: ")
        
        result = self.interface.show_loading(
            "[bold cyan]Fetching order details...[/bold cyan]",
            self.order.get_order_details,
            order_id=order_id
        )
        
        if result:
            key_columns = ['groww_order_id', 'trading_symbol', 'order_status', 'quantity', 
                          'price', 'transaction_type', 'order_type', 'created_at']
            self.interface.display_response(result, "Order Details", key_columns)
    
    def get_trades_details(self):
        """Get trades details for an order"""
        order_id = self.interface.input_prompt("Enter order ID: ")
        
        result = self.interface.show_loading(
            "[bold cyan]Fetching trades details...[/bold cyan]",
            self.order.get_trades_details,
            order_id=order_id
        )
        
        if result:
            self.interface.display_response(result, "Trade Details")
    
    def handle_portfolio_menu(self):
        """Handle portfolio menu"""
        menu_options = [
            "Get Portfolio Holdings",
            "Get Positions (CASH)",
            "Get Positions (FUTURES)",
            "Get All Positions",
            "Back to Main Menu"
        ]
        
        choice = self.interface.show_menu(menu_options, "Portfolio & Positions")
        
        if choice == "Get Portfolio Holdings":
            result = self.interface.show_loading(
                "[bold cyan]Fetching portfolio...[/bold cyan]",
                self.portfolio.get_portfolio
            )
            if result:
                self.interface.display_response(result, "Portfolio Holdings")
        
        elif choice == "Get Positions (CASH)":
            result = self.interface.show_loading(
                "[bold cyan]Fetching CASH positions...[/bold cyan]",
                self.portfolio.get_position_for_user,
                segment="CASH"
            )
            if result:
                self.interface.display_response(result, "CASH Positions")
        
        elif choice == "Get Positions (FUTURES)":
            result = self.interface.show_loading(
                "[bold cyan]Fetching FUTURES positions...[/bold cyan]",
                self.portfolio.get_position_for_user,
                segment="FUTURES"
            )
            if result:
                self.interface.display_response(result, "FUTURES Positions")
        
        elif choice == "Get All Positions":
            result = self.interface.show_loading(
                "[bold cyan]Fetching all positions...[/bold cyan]",
                self.portfolio.get_position_for_user
            )
            if result:
                self.interface.display_response(result, "All Positions")
    
    def handle_live_data_menu(self):
        """Handle live data menu"""
        menu_options = [
            "Get Live Quote",
            "Get LTP (Last Traded Price)",
            "Side-by-Side Comparison",
            "Back to Main Menu"
        ]
        
        choice = self.interface.show_menu(menu_options, "Live Market Data")
        
        if choice == "Get Live Quote":
            symbol = self.interface.input_prompt("Enter trading symbol: ")
            exchange = self.interface.input_prompt("Enter exchange (NSE/BSE): ", style="bold yellow") or "NSE"
            segment = self.interface.input_prompt("Enter segment (CASH/FUTURES): ", style="bold yellow") or "CASH"
            
            result = self.interface.show_loading(
                "[bold cyan]Fetching live quote...[/bold cyan]",
                self.live_data.get_live_quote,
                trading_symbol=symbol,
                exchange=exchange,
                segment=segment
            )
            
            if result:
                self.interface.display_response(result, f"Live Quote - {symbol}")
        
        elif choice == "Get LTP (Last Traded Price)":
            symbol = self.interface.input_prompt("Enter trading symbol: ")
            exchange = self.interface.input_prompt("Enter exchange (NSE/BSE): ", style="bold yellow") or "NSE"
            segment = self.interface.input_prompt("Enter segment (CASH/FUTURES): ", style="bold yellow") or "CASH"
            
            result = self.interface.show_loading(
                "[bold cyan]Fetching LTP...[/bold cyan]",
                self.live_data.get_ltp,
                trading_symbol=symbol,
                exchange=exchange,
                segment=segment
            )
            
            if result:
                self.interface.display_response(result, f"LTP - {symbol}")
        
        elif choice == "Side-by-Side Comparison":
            symbol1 = self.interface.input_prompt("Enter first symbol: ")
            symbol2 = self.interface.input_prompt("Enter second symbol: ")
            exchange = self.interface.input_prompt("Enter exchange (NSE/BSE): ", style="bold yellow") or "NSE"
            segment = self.interface.input_prompt("Enter segment (CASH/FUTURES): ", style="bold yellow") or "CASH"
            
            result1 = self.interface.show_loading(
                f"[bold cyan]Fetching {symbol1}...[/bold cyan]",
                self.live_data.get_live_quote,
                trading_symbol=symbol1,
                exchange=exchange,
                segment=segment
            )
            
            result2 = self.interface.show_loading(
                f"[bold cyan]Fetching {symbol2}...[/bold cyan]",
                self.live_data.get_live_quote,
                trading_symbol=symbol2,
                exchange=exchange,
                segment=segment
            )
            
            if result1 and result2:
                # Don't filter columns - show all available data for comparison
                self.interface.display_side_by_side(
                    result1, result2,
                    left_title=f"{symbol1} Quote",
                    right_title=f"{symbol2} Quote"
                    # Removed key_columns to show all available columns
                )
    
    def handle_search_menu(self):
        """Handle search menu"""
        query = self.interface.input_prompt("Enter search query: ")
        
        result = self.interface.show_loading(
            "[bold cyan]Searching instruments...[/bold cyan]",
            search_instrument,
            groww_symbol=query
        )
        
        if result:
            self.interface.display_response(result, "Search Results")
    
    def handle_vector_search_menu(self):
        """Handle AI vector search menu"""
        query = self.interface.input_prompt("Enter search query: ")
        
        result = self.interface.show_loading(
            "[bold cyan]AI is searching...[/bold cyan]",
            self.vector_search.search,
            query=query
        )
        
        if result:
            self.interface.display_response(result, "AI Vector Search Results")
