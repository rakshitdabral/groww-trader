# Groww Trader CLI

Groww Trader CLI is a robust, command-line interface application designed to facilitate trading on the Groww platform directly from your terminal. It provides a comprehensive suite of tools for order management, portfolio analysis, live market data tracking, and advanced AI-powered features like semantic search and a portfolio chatbot.

## 🚀 Features

### 1. 📊 Orders Management
Manage your orders with precision and ease.
- **Place Order**: Execute Buy orders for Equity (Cash) and F&O (Futures) segments.
- **Modify Order**: Update price and quantity for open orders.
- **Cancel Order**: Cancel pending orders instantly.
- **Get Order Status**: Check the real-time status of any order using its Order ID.
- **Get Order List**: View a list of your recent orders with key details like status, price, and quantity.
- **Get Order Details**: Retrieve comprehensive details for a specific order.
- **Get Trades Details**: access trade execution details associated with a specific order.

### 2. 💼 Portfolio & Positions
Keep a close eye on your investments and open positions.
- **Get Portfolio Holdings**: View all your current long-term holdings.
- **Get Positions (CASH)**: Monitor your intraday positions in the Cash segment.
- **Get Positions (FUTURES)**: Track your open positions in the Futures segment.
- **Get All Positions**: detailed view of all open positions across segments.

### 3. 📈 Live Market Data
Stay updated with real-time market information.
- **Get Live Quote**: Fetch real-time quotes for stocks on NSE/BSE.
- **Get LTP (Last Traded Price)**: Quickly check the latest price for any instrument.
- **Side-by-Side Comparison**: Compare live quotes of two different stocks side-by-side for better decision making.

### 4. 🔍 Search Instruments
- **Search**: Find trading instruments and their script codes on NSE and BSE using keywords (e.g., "RELIANCE", "TCS").

### 5. 🤖 AI Vector Search
Leverage the power of AI to find relevant financial information.
- **Semantic Search**: Use natural language queries to search through indexed financial data using Pinecone and OpenAI embeddings.

### 6. 💬 Portfolio Chatbot
Interact with your portfolio using an intelligent AI assistant.
- **Context-Aware**: The chatbot has access to your real-time portfolio holdings and positions.
- **Reasoning Capabilities**: Ask complex analytical questions about your investments (e.g., "What is my best performing stock?", "Calculate total portfolio value").
- **Powered by OpenAI**: Utilizes GPT-4o-mini and o1-preview models for accurate and insightful responses.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)

You will also need valid API keys and credentials for:
- **Groww**: API Key, API Secret, and an Access Token.
- **OpenAI**: API Key (for AI features).
- **Pinecone**: API Key and Index Name (for Vector Search).

## 📥 Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd Groww-Trader
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The project uses `growwapi`, `pinecone-client`, `openai`, `sentence-transformers`, `rich`, `inquirer`, and other libraries.*

4.  **Install the Package in Editable Mode**
    ```bash
    pip install -e .
    ```

## ⚙️ Configuration

Create a `.env` file in the root directory of the project and add your credentials. You can use the following template:

```env
# Groww API Credentials
GROWW_API_KEY=your_groww_api_key
GROWW_API_SECRET=your_groww_api_secret
# Note: Access token handling is automated via 'grow_trader/utils/groww_utils/authentication.py'
# You might need to implement/configure 'get_grow_access_token' depending on your auth flow.

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_EMBEDDING_DIMENSION=1536

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME_EQ=your_index_name
```

## 🖥️ Usage

To start the application, run `main.py`:

```bash
python main.py
```

### Navigation
The application uses an interactive menu system powered by `inquirer` and `rich`.
- Use **Arrow Keys** to navigate through menu options.
- Press **Enter** to select an option.
- Follow on-screen prompts to enter inputs (e.g., symbols, prices, quantities).

### Example Workflow
1.  Select **"📈 Live Market Data"** -> **"Get Live Quote"**.
2.  Enter Symbol: `INFY`.
3.  Enter Exchange: `NSE`.
4.  View the real-time quote.
5.  Go back to Main Menu.
6.  Select **"📊 Orders Management"** -> **"Place Order"**.
7.  Enter Symbol: `INFY`, Quantity: `1`, Price: `1500`.
8.  Confirm and place the order.

## 📂 Project Structure

```
Groww-Trader/
├── Artifacts/              # Generated artifacts
├── Notebooks/              # Jupyter notebooks for analysis/experiments
├── Trading_Data/           # Data storage for trading activities
├── grow_trader/            # Main package source code
│   ├── cli/                # CLI interface and logic
│   │   ├── app.py          # Main CLI application class
│   │   └── interface.py    # UI/UX components (menus, displays)
│   ├── config/             # Configuration files
│   │   ├── groww_config.py
│   │   ├── openai_config.py
│   │   └── pinecone_config.py
│   ├── core/               # Core business logic
│   │   ├── groww_order.py        # Order management logic
│   │   ├── groww_portfolio.py    # Portfolio management logic
│   │   ├── groww_live_data.py    # Live market data logic
│   │   ├── portfolio_chatbot.py  # AI Chatbot implementation
│   │   └── vector_db_search.py   # Vector search implementation
│   ├── exception/          # Custom exception handling
│   ├── logging/            # Logging configuration
│   └── utils/              # Utility functions
│       └── groww_utils/
│           ├── authentication.py
│           └── search_instrument.py
├── main.py                 # Entry point script
├── requirements.txt        # Project dependencies
└── setup.py                # Package setup file
```

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the project, please follow these steps:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## 📞 Contact

**Author**: Rakshit Dabral
**Email**: rakshitdabral1@gmail.com

---
*Disclaimer: This tool is for educational and assistance purposes. Trading involves financial risk. Please ensure you understand the risks and test thoroughly before using with real capital.*
