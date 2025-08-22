# Stock Trading Expert Agent 📈

An intelligent stock trading analysis agent that combines real-time market data from Yahoo Finance with AI-powered analysis using OpenAI's GPT-4 to provide investment recommendations.

## Features 🚀

- **Real-time Stock Data**: Fetches current prices, volume, P/E ratios, 52-week ranges, and more from Yahoo Finance
- **AI-Powered Analysis**: Uses GPT-4 to analyze stock data and provide BUY/HOLD/SELL recommendations
- **Comprehensive Metrics**: Tracks price movements, valuation metrics, trading activity, and market sentiment
- **Detailed Recommendations**: Provides confidence levels, key factors, and detailed reasoning for each recommendation
- **Interactive & Batch Modes**: Analyze single stocks interactively or multiple stocks in batch mode

## Installation 📦

1. Clone the repository:
```bash
git clone <your-repo-url>
cd stock-trading-experiment-agent-py
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage 🎯

### Quick Start

```python
from stock_trading_agent import StockTradingAgent

# Initialize the agent
agent = StockTradingAgent()

# Analyze a stock
result = agent.analyze_stock('AAPL')

# Print the recommendation summary
print(agent.get_recommendation_summary(result))
```

### Interactive Mode

Run the agent in interactive mode to analyze stocks one by one:

```bash
python example.py --interactive
```

Example session:
```
🚀 Stock Trading Expert Agent - Interactive Mode
============================================================
Enter a stock symbol to analyze (or 'quit' to exit)
============================================================

📊 Enter stock symbol: AAPL

🔍 Analyzing AAPL...
✅ Retrieved stock data for Apple Inc.
💰 Current Price: $178.25
📊 Week Change: 2.34%
📈 Month Change: 5.67%

🤖 Analyzing with AI...

============================================================
📊 STOCK ANALYSIS REPORT
============================================================

🏢 Company: Apple Inc. (AAPL)
💵 Current Price: $178.25

🟢 RECOMMENDATION: BUY
📊 Confidence Level: HIGH

🔑 Key Factors:
  • Strong weekly momentum
  • Attractive P/E ratio
  • Near 52-week high

📝 Detailed Analysis:
------------------------------------------------------------
Based on the comprehensive analysis of Apple Inc. (AAPL), I recommend a BUY. The stock shows strong momentum with a 2.34% gain over the past week and an impressive 5.67% increase over the past month...
------------------------------------------------------------
```

### Batch Mode

Analyze multiple stocks at once:

```bash
python example.py
```

This will analyze a predefined list of stocks (AAPL, GOOGL, TSLA, MSFT, AMZN) and display recommendations for each.

### Programmatic Usage

```python
from stock_trading_agent import StockTradingAgent
import os

# Method 1: Using environment variable
os.environ['OPENAI_API_KEY'] = 'your_api_key'
agent = StockTradingAgent()

# Method 2: Pass API key directly
agent = StockTradingAgent(openai_api_key='your_api_key')

# Analyze multiple stocks
stocks = ['NVDA', 'META', 'NFLX']
for symbol in stocks:
    result = agent.analyze_stock(symbol)
    if result['success']:
        print(f"{symbol}: {result['recommendation']} - {result['confidence']} confidence")
        print(f"Analysis: {result['analysis'][:200]}...")
    else:
        print(f"Failed to analyze {symbol}: {result['error']}")
```

## API Reference 📚

### StockTradingAgent

#### `__init__(openai_api_key: Optional[str] = None)`
Initialize the agent with an optional OpenAI API key. If not provided, it will look for `OPENAI_API_KEY` in environment variables.

#### `analyze_stock(symbol: str) -> Dict[str, Any]`
Analyze a stock and return comprehensive analysis with recommendation.

**Returns:**
```python
{
    'success': bool,
    'symbol': str,
    'company_name': str,
    'current_price': float,
    'recommendation': 'BUY' | 'HOLD' | 'SELL',
    'confidence': 'HIGH' | 'MEDIUM' | 'LOW',
    'analysis': str,  # Detailed AI analysis
    'key_factors': List[str],
    'stock_data': Dict  # Complete stock data
}
```

#### `get_recommendation_summary(result: Dict[str, Any]) -> str`
Format the analysis result into a human-readable summary report.

## Stock Data Provided 📊

The agent fetches and analyzes the following metrics:

- **Price Data**: Current price, open, high, low, previous close
- **Price Changes**: 1-week and 1-month percentage changes
- **52-Week Range**: Yearly high and low prices
- **Volume**: Current volume and average volume
- **Valuation**: P/E ratio, Forward P/E, EPS, Market Cap
- **Dividend**: Dividend yield (if applicable)
- **Risk Metrics**: Beta coefficient
- **Sector Information**: Industry and sector classification
- **Analyst Ratings**: Current analyst recommendations

## Examples 💡

### Example 1: Analyzing Tech Stocks

```python
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA']
recommendations = {}

for stock in tech_stocks:
    result = agent.analyze_stock(stock)
    if result['success']:
        recommendations[stock] = {
            'action': result['recommendation'],
            'price': result['current_price'],
            'confidence': result['confidence']
        }

# Find strong buy recommendations
strong_buys = [s for s, r in recommendations.items() 
               if r['action'] == 'BUY' and r['confidence'] == 'HIGH']
print(f"Strong Buy Recommendations: {', '.join(strong_buys)}")
```

### Example 2: Portfolio Analysis

```python
portfolio = {
    'AAPL': 50,   # 50 shares
    'GOOGL': 20,  # 20 shares
    'TSLA': 30    # 30 shares
}

total_value = 0
for symbol, shares in portfolio.items():
    result = agent.analyze_stock(symbol)
    if result['success']:
        value = result['current_price'] * shares
        total_value += value
        print(f"{symbol}: {shares} shares @ ${result['current_price']} = ${value:.2f}")
        print(f"  Recommendation: {result['recommendation']} ({result['confidence']})")

print(f"\nTotal Portfolio Value: ${total_value:.2f}")
```

### Example 3: Custom Analysis

```python
# Analyze and filter by specific criteria
def find_value_stocks(symbols, max_pe=20, min_dividend=0.02):
    value_stocks = []
    
    for symbol in symbols:
        result = agent.analyze_stock(symbol)
        if result['success']:
            data = result['stock_data']
            pe = data['pe_ratio']
            dividend = data['dividend_yield']
            
            if pe > 0 and pe < max_pe and dividend >= min_dividend:
                value_stocks.append({
                    'symbol': symbol,
                    'pe_ratio': pe,
                    'dividend_yield': dividend * 100,
                    'recommendation': result['recommendation']
                })
    
    return value_stocks

# Find value stocks with P/E < 20 and dividend yield > 2%
value_picks = find_value_stocks(['KO', 'JNJ', 'VZ', 'T', 'IBM'])
for stock in value_picks:
    print(f"{stock['symbol']}: P/E={stock['pe_ratio']:.1f}, "
          f"Dividend={stock['dividend_yield']:.2f}%, "
          f"Rec={stock['recommendation']}")
```

## Error Handling 🛡️

The agent includes comprehensive error handling:

```python
result = agent.analyze_stock('INVALID_SYMBOL')
if not result['success']:
    print(f"Error: {result['error']}")
    # Handle the error appropriately
```

Common errors:
- Invalid stock symbol
- Network connectivity issues
- API rate limits
- Invalid API key

## Requirements 📋

- Python 3.7+
- Active internet connection
- OpenAI API key with GPT-4 access
- Dependencies listed in `requirements.txt`

## Limitations ⚠️

- Stock data is real-time but may have slight delays
- AI recommendations are based on available data and should not be the sole basis for investment decisions
- API rate limits apply to both Yahoo Finance and OpenAI
- Some international stocks may have limited data availability

## Disclaimer 📝

This tool is for educational and informational purposes only. It should not be considered as financial advice. Always do your own research and consult with qualified financial advisors before making investment decisions.

## Contributing 🤝

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.