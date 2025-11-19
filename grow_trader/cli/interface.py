import sys
import time
from typing import Any, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich import box
import pandas as pd
import json

console = Console()

class CLInterface:
    """Interactive Command Line Interface with rich formatting"""
    
    def __init__(self):
        self.console = Console()
        self.layout = None
        
    def print_banner(self):
        """Display ASCII art banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      ██████╗ ██████╗  ██████╗ ██╗    ██╗ ██╗    ██╗          ║
║      ██╔════╝██╔══██╗██╔═══██╗██║    ██║ ██║    ██║          ║
║      ██║  ███╗██████╔╝██║   ██║██║ █╗ ██║ ██║ █╗ ██║         ║
║      ██║   ██║██╔══██╗██║   ██║██║███╗██║ ██║███╗██║         ║
║      ╚██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝ ╚███╔███╔╝         ║
║       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝   ╚══╝╚══╝          ║
║                                                              ║
║      T R A D E R   C O M M A N D   C E N T E R               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")
        
    def typing_effect(self, text: str, delay: float = 0.03, style: str = "white"):
        """Display text with typing animation"""
        for char in text:
            self.console.print(char, end="", style=style)
            time.sleep(delay)
        self.console.print()  # New line after typing
        
    def show_loading(self, message: str = "Processing request...", func: Optional[Callable] = None, *args, **kwargs):
        """Show loading spinner while executing a function"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(message, total=None)
            
            if func:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
                    return None
            else:
                # Just show spinner for a bit
                time.sleep(1)
                return None
                
    def create_table(self, data: Any, title: str = "Response", key_columns: Optional[list] = None, max_width: Optional[int] = None) -> Table:
        """Convert data to Rich Table format"""
        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")
        
        # Columns to exclude from display
        exclude_columns = ['depth']
        
        # Handle dictionary responses
        if isinstance(data, dict):
            list_keys = [key for key, value in data.items() 
                        if isinstance(value, list) and len(value) > 0]
            
            if list_keys:
                # Multiple lists - create separate tables for each
                for list_key in list_keys:
                    df = pd.DataFrame(data[list_key])
                    
                    # Remove excluded columns
                    df = df.drop(columns=[col for col in exclude_columns if col in df.columns], errors='ignore')
                    
                    if key_columns:
                        available_columns = [col for col in key_columns if col in df.columns]
                        if available_columns:
                            df_display = df[available_columns]
                        else:
                            df_display = df
                    else:
                        df_display = df
                    
                    # Create columns with proper width constraints
                    for col in df_display.columns:
                        # Set max width for columns if specified, otherwise use auto
                        col_width = None
                        if max_width:
                            # Distribute width evenly, but cap at reasonable max
                            col_width = min(max_width // len(df_display.columns), 30)
                        table.add_column(
                            col, 
                            style="cyan", 
                            no_wrap=False,
                            max_width=col_width,
                            overflow="fold"
                        )
                    
                    # Add rows
                    for _, row in df_display.iterrows():
                        table.add_row(*[str(val) for val in row.values])
                    
                    return table
            else:
                # Single dictionary
                df = pd.DataFrame([data])
                
                # Remove excluded columns
                df = df.drop(columns=[col for col in exclude_columns if col in df.columns], errors='ignore')
                
                if key_columns:
                    available_columns = [col for col in key_columns if col in df.columns]
                    if available_columns:
                        df_display = df[available_columns]
                    else:
                        df_display = df
                else:
                    df_display = df
                
                for col in df_display.columns:
                    col_width = None
                    if max_width:
                        col_width = min(max_width // len(df_display.columns), 30)
                    table.add_column(
                        col, 
                        style="cyan", 
                        no_wrap=False,
                        max_width=col_width,
                        overflow="fold"
                    )
                
                for _, row in df_display.iterrows():
                    table.add_row(*[str(val) for val in row.values])
                
                return table
        
        # Handle list responses
        elif isinstance(data, list):
            if data:
                df = pd.DataFrame(data)
                
                # Remove excluded columns
                df = df.drop(columns=[col for col in exclude_columns if col in df.columns], errors='ignore')
                
                if key_columns:
                    available_columns = [col for col in key_columns if col in df.columns]
                    if available_columns:
                        df_display = df[available_columns]
                    else:
                        df_display = df
                else:
                    df_display = df
                
                for col in df_display.columns:
                    col_width = None
                    if max_width:
                        col_width = min(max_width // len(df_display.columns), 30)
                    table.add_column(
                        col, 
                        style="cyan", 
                        no_wrap=False,
                        max_width=col_width,
                        overflow="fold"
                    )
                
                for _, row in df_display.iterrows():
                    table.add_row(*[str(val) for val in row.values])
                
                return table
            else:
                table.add_column("Status", style="yellow")
                table.add_row("No data found")
                return table
        
        # Fallback for other types
        else:
            table.add_column("Data", style="cyan")
            table.add_row(json.dumps(data, indent=2))
            return table
    
    def display_response(self, data: Any, title: str = "Response", key_columns: Optional[list] = None):
        """Display response in a formatted panel with table"""
        table = self.create_table(data, title, key_columns)
        panel = Panel(
            table,
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def create_side_by_side_layout(self, left_content: str, right_content: str):
        """Create side-by-side layout"""
        layout = Layout()
        layout.split_row(
            Layout(Panel(left_content, title="[bold blue]Left Panel[/bold blue]", border_style="blue")),
            Layout(Panel(right_content, title="[bold yellow]Right Panel[/bold yellow]", border_style="yellow"))
        )
        return layout
    
    def display_side_by_side(self, left_data: Any, right_data: Any, 
                            left_title: str = "Left", right_title: str = "Right",
                            left_key_columns: Optional[list] = None,
                            right_key_columns: Optional[list] = None):
        """Display two responses stacked vertically (one below the other)"""
        # Get terminal width for better column sizing
        terminal_width = self.console.width or 120
        # Use full width minus padding for better readability
        available_width = terminal_width - 10
        
        # For comparison, show all columns by default if key_columns don't match well
        # First, let's check what columns are actually available
        left_df = None
        right_df = None
        
        # Convert data to DataFrame to inspect columns
        if isinstance(left_data, dict):
            list_keys = [key for key, value in left_data.items() 
                        if isinstance(value, list) and len(value) > 0]
            if list_keys:
                left_df = pd.DataFrame(left_data[list_keys[0]])
            else:
                left_df = pd.DataFrame([left_data])
        elif isinstance(left_data, list):
            left_df = pd.DataFrame(left_data) if left_data else None
        
        if isinstance(right_data, dict):
            list_keys = [key for key, value in right_data.items() 
                        if isinstance(value, list) and len(value) > 0]
            if list_keys:
                right_df = pd.DataFrame(right_data[list_keys[0]])
            else:
                right_df = pd.DataFrame([right_data])
        elif isinstance(right_data, list):
            right_df = pd.DataFrame(right_data) if right_data else None
        
        # If key_columns are provided, check if they match well
        # If less than 30% match, show all columns instead
        if left_key_columns and left_df is not None:
            available_cols = [col for col in left_key_columns if col in left_df.columns]
            if len(available_cols) < max(1, len(left_key_columns) * 0.3):
                # Not enough matches, show all columns
                left_key_columns = None
        
        if right_key_columns and right_df is not None:
            available_cols = [col for col in right_key_columns if col in right_df.columns]
            if len(available_cols) < max(1, len(right_key_columns) * 0.3):
                # Not enough matches, show all columns
                right_key_columns = None
        
        # Create tables with full width (no max_width constraint for better readability)
        left_table = self.create_table(left_data, left_title, left_key_columns, max_width=available_width)
        right_table = self.create_table(right_data, right_title, right_key_columns, max_width=available_width)
        
        # Always display tables stacked vertically (one below the other)
        self.console.print(Panel(left_table, title=f"[bold blue]{left_title}[/bold blue]", border_style="blue"))
        self.console.print("\n")  # Add spacing between tables
        self.console.print(Panel(right_table, title=f"[bold yellow]{right_title}[/bold yellow]", border_style="yellow"))
        
    def show_menu(self, options: list, title: str = "Menu") -> str:
        """Display interactive menu"""
        self.console.print(f"\n[bold cyan]{title}[/bold cyan]")
        self.console.print("=" * 60)
        
        for idx, option in enumerate(options, 1):
            self.console.print(f"[green]{idx}.[/green] {option}")
        
        self.console.print("=" * 60)
        
        while True:
            try:
                choice = self.console.input("[bold yellow]Enter your choice: [/bold yellow]")
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                else:
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number.[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                sys.exit(0)
    
    def input_prompt(self, prompt: str, style: str = "bold yellow") -> str:
        """Get user input with styled prompt"""
        return self.console.input(f"[{style}]{prompt}[/{style}]")
    
    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"[bold green]✓ {message}[/bold green]")
    
    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"[bold red]✗ {message}[/bold red]")
    
    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"[bold blue]ℹ {message}[/bold blue]")
    
    def clear_screen(self):
        """Clear the console"""
        self.console.clear()
