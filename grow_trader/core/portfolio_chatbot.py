import os
import sys
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

from grow_trader.core.groww_portfolio import GrowwPortfolio
from grow_trader.config.openai_config import OPENAI_API_KEY
from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException
from grow_trader.utils.groww_utils.authentication import get_grow_access_token

load_dotenv()

class PortfolioChatbot:
    """Chatbot for interacting with portfolio data using OpenAI"""
    
    def __init__(self, groww_auth_token: str = get_grow_access_token(), use_reasoning_model: bool = False):
        self.portfolio = GrowwPortfolio(groww_auth_token)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.conversation_history: List[Dict[str, str]] = []
        self.portfolio_data: Optional[Dict[str, Any]] = None
        self.positions_data: Optional[Dict[str, Any]] = None
        self.use_reasoning_model = use_reasoning_model
        self.reasoning_model = "o1-preview"
        self.standard_model = "gpt-4o-mini"
        
    def _load_portfolio_data(self):
        """Load portfolio and positions data"""
        try:
            if self.portfolio_data is None:
                logging.info("Loading portfolio holdings data...")
                self.portfolio_data = self.portfolio.get_portfolio()
                logging.info(f"Portfolio data loaded: {type(self.portfolio_data)}")
                if self.portfolio_data:
                    if isinstance(self.portfolio_data, dict):
                        logging.info(f"Portfolio data keys: {list(self.portfolio_data.keys())}")
                    elif isinstance(self.portfolio_data, list):
                        logging.info(f"Portfolio data length: {len(self.portfolio_data)}")
        except Exception as e:
            logging.error(f"Could not load portfolio holdings: {str(e)}")
            self.portfolio_data = {}
        
        try:
            if self.positions_data is None:
                logging.info("Loading positions data...")
                self.positions_data = self.portfolio.get_position_for_user()
                logging.info(f"Positions data loaded: {type(self.positions_data)}")
                if self.positions_data:
                    if isinstance(self.positions_data, dict):
                        logging.info(f"Positions data keys: {list(self.positions_data.keys())}")
                    elif isinstance(self.positions_data, list):
                        logging.info(f"Positions data length: {len(self.positions_data)}")
        except Exception as e:
            logging.error(f"Could not load positions: {str(e)}")
            self.positions_data = {}
    
    def _format_portfolio_context(self) -> str:
        """Format portfolio data as context for the chatbot"""
        self._load_portfolio_data()
        
        context_parts = []
        
        # Format holdings
        if self.portfolio_data:
            if isinstance(self.portfolio_data, dict):
                # Check if it has a list of holdings
                holdings = None
                for key, value in self.portfolio_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        holdings = value
                        break
                
                if holdings:
                    context_parts.append("PORTFOLIO HOLDINGS:")
                    context_parts.append(f"Total holdings: {len(holdings)}")
                    for idx, holding in enumerate(holdings[:50], 1):  # Limit to first 50 for context
                        holding_str = ", ".join([f"{k}: {v}" for k, v in holding.items() if v is not None])
                        context_parts.append(f"{idx}. {holding_str}")
                    if len(holdings) > 50:
                        context_parts.append(f"... and {len(holdings) - 50} more holdings")
                else:
                    # Single holding or different structure - try to format nicely
                    if len(self.portfolio_data) > 0:
                        context_parts.append("PORTFOLIO HOLDINGS:")
                        # Try to format as a readable string
                        formatted_data = json.dumps(self.portfolio_data, indent=2, default=str)
                        context_parts.append(formatted_data)
            elif isinstance(self.portfolio_data, list):
                if len(self.portfolio_data) > 0:
                    context_parts.append("PORTFOLIO HOLDINGS:")
                    context_parts.append(f"Total holdings: {len(self.portfolio_data)}")
                    for idx, holding in enumerate(self.portfolio_data[:50], 1):
                        if isinstance(holding, dict):
                            holding_str = ", ".join([f"{k}: {v}" for k, v in holding.items() if v is not None])
                            context_parts.append(f"{idx}. {holding_str}")
                        else:
                            context_parts.append(f"{idx}. {holding}")
                    if len(self.portfolio_data) > 50:
                        context_parts.append(f"... and {len(self.portfolio_data) - 50} more holdings")
        
        # Format positions
        if self.positions_data:
            if isinstance(self.positions_data, dict):
                positions = None
                for key, value in self.positions_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        positions = value
                        break
                
                if positions:
                    context_parts.append("\nCURRENT POSITIONS:")
                    context_parts.append(f"Total positions: {len(positions)}")
                    for idx, position in enumerate(positions[:50], 1):
                        if isinstance(position, dict):
                            position_str = ", ".join([f"{k}: {v}" for k, v in position.items() if v is not None])
                            context_parts.append(f"{idx}. {position_str}")
                        else:
                            context_parts.append(f"{idx}. {position}")
                    if len(positions) > 50:
                        context_parts.append(f"... and {len(positions) - 50} more positions")
                else:
                    if len(self.positions_data) > 0:
                        context_parts.append("\nCURRENT POSITIONS:")
                        formatted_data = json.dumps(self.positions_data, indent=2, default=str)
                        context_parts.append(formatted_data)
            elif isinstance(self.positions_data, list):
                if len(self.positions_data) > 0:
                    context_parts.append("\nCURRENT POSITIONS:")
                    context_parts.append(f"Total positions: {len(self.positions_data)}")
                    for idx, position in enumerate(self.positions_data[:50], 1):
                        if isinstance(position, dict):
                            position_str = ", ".join([f"{k}: {v}" for k, v in position.items() if v is not None])
                            context_parts.append(f"{idx}. {position_str}")
                        else:
                            context_parts.append(f"{idx}. {position}")
                    if len(self.positions_data) > 50:
                        context_parts.append(f"... and {len(self.positions_data) - 50} more positions")
        
        if not context_parts:
            return "No portfolio data available. The user's portfolio appears to be empty or data could not be loaded."
        
        return "\n".join(context_parts)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the chatbot with enhanced instructions and reasoning guidelines"""
        portfolio_context = self._format_portfolio_context()
        
        return f"""You are an expert financial portfolio assistant chatbot with advanced analytical capabilities. Your role is to help users understand, analyze, and make informed decisions about their investment portfolio.

=== PORTFOLIO DATA CONTEXT ===
IMPORTANT: You have access to the user's ACTUAL portfolio holdings and current positions. The data below is REAL and CURRENT. Always reference this data when answering questions.

{portfolio_context}

=== CORE INSTRUCTIONS ===

0. SCOPE & LIMITATIONS (CRITICAL):
   - You are EXCLUSIVELY a portfolio and investment assistant
   - ONLY answer questions related to:
     * Portfolio holdings, positions, and investments
     * Stock analysis, performance, and valuation
     * Portfolio calculations, diversification, and risk analysis
     * Investment strategies and portfolio management
     * Financial data from the user's portfolio
     * Financial/portfolio terminology and concepts (e.g., T1/T2 settlement, demat, pledge, ISIN, trading symbols, etc.)
     * Educational questions about how portfolio/trading concepts work
     * Questions about terms or fields that appear in the portfolio data (e.g., "What is T1 quantity?", "What does pledge quantity mean?")
   - DO NOT answer questions about:
     * General knowledge unrelated to finance (geography, history, science, general trivia, etc.)
     * Non-financial topics (sports, entertainment, cooking, etc.)
     * Questions completely unrelated to investments, portfolio, or financial markets
   - If asked a question NOT related to portfolio/investments/finance:
     * Politely decline: "I'm a portfolio assistant and can only help with questions about your investments, portfolio, or financial concepts. Could you please ask me something about your holdings, positions, investment analysis, or portfolio-related terms?"
     * Do NOT provide any answer to the unrelated question
     * Redirect the conversation back to portfolio/investment topics

1. DATA ACCURACY & REFERENCE:
   - ALWAYS use the portfolio data provided above to answer questions about holdings
   - When asked about holdings, positions, or specific stocks, look them up in the PORTFOLIO DATA section above
   - If the data shows holdings/positions, reference them directly - do NOT say you don't have access
   - Provide specific details from the data (stock names, quantities, values, prices, etc.)
   - If the data shows "No portfolio data available", inform the user their portfolio appears empty

2. REASONING & ANALYSIS PROCESS:
   - For analytical questions, follow a structured reasoning approach:
     a) First, identify what data is needed from the portfolio
     b) Extract the relevant information from the PORTFOLIO DATA section
     c) Perform calculations step-by-step (totals, percentages, comparisons, etc.)
     d) Verify your calculations before presenting results
     e) Provide clear explanations of your reasoning
   
   - For complex queries (e.g., "What's my best performing stock?", "Calculate my total portfolio value"):
     * Break down the question into smaller components
     * Identify all relevant holdings/positions
     * Extract numerical values (quantities, prices, values)
     * Perform calculations methodically
     * Present results with context and interpretation

3. CALCULATIONS & COMPUTATIONS:
   - Always calculate totals, percentages, or comparisons using the actual data provided
   - Show your work when performing calculations (e.g., "Total value = quantity × price = ...")
   - Round numbers appropriately (typically 2 decimal places for currency, percentages)
   - Double-check arithmetic to ensure accuracy
   - When comparing holdings, use consistent units and timeframes

4. RESPONSE QUALITY:
   - Be concise but informative - provide enough detail to be helpful
   - Use natural, conversational language - avoid overly technical jargon unless the user asks for it
   - Format numbers and percentages clearly (e.g., ₹1,23,456.78 or 12.34%)
   - Use bullet points or structured formatting for lists of holdings
   - Highlight important insights or anomalies in the data

5. PORTFOLIO ANALYSIS CAPABILITIES:
   - Identify top/bottom performers by value or percentage change
   - Calculate portfolio diversification (sector distribution, asset allocation)
   - Compare current positions vs holdings
   - Identify concentration risks (if any single holding is >20% of portfolio)
   - Calculate total portfolio value and individual holding percentages
   - Provide insights on portfolio health and balance

6. ERROR HANDLING:
   - If data is missing or unclear, acknowledge it and work with available information
   - If calculations cannot be performed due to missing data, explain what's needed
   - Never make up or assume data that isn't in the PORTFOLIO DATA section

=== REASONING GUIDELINES ===

When answering questions, especially analytical ones:
1. CHECK if the question is related to portfolio/investments/finance:
   - Questions about portfolio holdings, stocks, investments = YES, answer
   - Questions about financial/portfolio terminology (T1, T2, demat, pledge, ISIN, etc.) = YES, answer
   - Questions about how portfolio/trading concepts work = YES, answer
   - Questions about terms that appear in the PORTFOLIO DATA = YES, answer (e.g., "What is T1 quantity?" when T1 Quantity appears in the data)
   - General knowledge questions (geography, history, etc.) = NO, politely decline
2. READ the question carefully and identify what is being asked (only if portfolio/finance-related)
3. LOCATE relevant data in the PORTFOLIO DATA section (if applicable)
4. EXTRACT the necessary values (quantities, prices, names, etc.) or explain the concept
5. REASON through the problem step-by-step
6. CALCULATE using the extracted data (if calculation needed)
7. VERIFY your calculations (if calculation needed)
8. PRESENT results clearly with appropriate context

Remember: 
- The PORTFOLIO DATA section above contains the user's actual holdings. Always use it to answer their questions.
- You are ONLY a portfolio assistant - only answer questions about investments, portfolio, stocks, and financial matters.
- For any non-portfolio questions, politely decline and redirect to portfolio-related topics.
- Be precise, methodical, and helpful, but stay within your scope as a portfolio assistant."""
    
    def chat(self, user_message: str, refresh_data: bool = False) -> str:
        """Chat with the portfolio chatbot"""
        try:
            # Refresh data if requested or if we don't have any data yet
            if refresh_data or self.portfolio_data is None:
                if refresh_data:
                    logging.info("Refreshing portfolio data...")
                else:
                    logging.info("Loading portfolio data for first time...")
                self.portfolio_data = None
                self.positions_data = None
            
            # Load portfolio data (will use cache if already loaded and refresh_data=False)
            self._load_portfolio_data()
            
            # Log what we got
            portfolio_context = self._format_portfolio_context()
            logging.info(f"Portfolio context length: {len(portfolio_context)} characters")
            if "No portfolio data" not in portfolio_context and len(portfolio_context) > 100:
                logging.info("Portfolio data successfully loaded and formatted")
            else:
                logging.warning("No portfolio data available - portfolio may be empty or could not be loaded")
            
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare messages for OpenAI - always include fresh system prompt with current data
            # This ensures the AI always has the latest portfolio context
            system_prompt = self._get_system_prompt()
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
            
            # Add conversation history (keep last 10 exchanges to manage token usage)
            messages.extend(self.conversation_history[-10:])
            
            # Determine which model to use based on reasoning requirements
            # Reasoning models (o1-preview/o1-mini) are better for complex analysis but don't support system messages
            # Standard models support system messages and are faster for simple queries
            if self.use_reasoning_model:
                # Reasoning models don't support system messages, so we need to prepend system prompt to user message
                # Also, reasoning models don't support temperature parameter
                # For o1 models, we only send user messages (they handle reasoning internally)
                # Extract conversation history (excluding system message)
                conversation_only = [msg for msg in messages if msg["role"] != "system"]
                
                if conversation_only:
                    # Get the last user message (current question)
                    last_user_msg = conversation_only[-1] if conversation_only[-1]["role"] == "user" else None
                    
                    if last_user_msg:
                        # Combine system prompt with the current user message
                        combined_user_content = f"{system_prompt}\n\nUser Question: {last_user_msg['content']}"
                        
                        # Build reasoning messages: previous conversation + current question with system prompt
                        reasoning_messages = []
                        # Add previous conversation pairs (excluding the last user message we're about to replace)
                        for i in range(len(conversation_only) - 1):
                            reasoning_messages.append(conversation_only[i])
                        # Add the current user message with system prompt prepended
                        reasoning_messages.append({"role": "user", "content": combined_user_content})
                        
                        response = self.client.chat.completions.create(
                            model=self.reasoning_model,
                            messages=reasoning_messages,
                            max_tokens=2000  # Reasoning models may need more tokens for complex reasoning
                        )
                    else:
                        # Fallback to standard model if no user message found
                        logging.warning("No user message found for reasoning model, falling back to standard model")
                        response = self.client.chat.completions.create(
                            model=self.standard_model,
                            messages=messages,
                            temperature=0.3,
                            max_tokens=2000
                        )
                else:
                    # Fallback to standard model if no conversation history
                    logging.warning("No conversation history for reasoning model, falling back to standard model")
                    response = self.client.chat.completions.create(
                        model=self.standard_model,
                        messages=messages,
                        temperature=0.3,
                        max_tokens=2000
                    )
            else:
                # Use standard model with enhanced system prompt
                # Lower temperature (0.3) for better reasoning and more focused responses
                # Higher max_tokens for detailed analytical responses
                response = self.client.chat.completions.create(
                    model=self.standard_model,
                    messages=messages,
                    temperature=0.3,  # Reduced from 0.7 for better analytical reasoning
                    max_tokens=2000  # Increased to allow more detailed responses and calculations
                )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error in chatbot: {str(e)}"
            logging.error(error_msg, exc_info=True)
            raise CustomException(error_msg, sys)
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        logging.info("Conversation history reset")
    
    def enable_reasoning_mode(self):
        """Enable reasoning model for complex analytical queries"""
        self.use_reasoning_model = True
        logging.info(f"Reasoning mode enabled using model: {self.reasoning_model}")
    
    def disable_reasoning_mode(self):
        """Disable reasoning model and use standard model"""
        self.use_reasoning_model = False
        logging.info(f"Reasoning mode disabled, using standard model: {self.standard_model}")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history."
        
        user_messages = [msg["content"] for msg in self.conversation_history if msg["role"] == "user"]
        return f"Total exchanges: {len(user_messages)}. Topics discussed: {', '.join(user_messages[:5])}"