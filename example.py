from stock_trading_agent import StockTradingAgent
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    
    agent = StockTradingAgent()
    
    print("🚀 Stock Trading Expert Agent")
    print("=" * 60)
    
    stocks_to_analyze = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']
    
    print(f"\n📋 Analyzing {len(stocks_to_analyze)} stocks: {', '.join(stocks_to_analyze)}")
    print("=" * 60)
    
    for symbol in stocks_to_analyze:
        result = agent.analyze_stock(symbol)
        print(agent.get_recommendation_summary(result))
        print("\n" + "="*60 + "\n")
        
        input("Press Enter to analyze the next stock...")


def interactive_mode():
    load_dotenv()
    
    agent = StockTradingAgent()
    
    print("🚀 Stock Trading Expert Agent - Interactive Mode")
    print("=" * 60)
    print("Enter a stock symbol to analyze (or 'quit' to exit)")
    print("=" * 60)
    
    while True:
        symbol = input("\n📊 Enter stock symbol: ").strip()
        
        if symbol.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thank you for using Stock Trading Expert Agent!")
            break
            
        if not symbol:
            print("❌ Please enter a valid stock symbol")
            continue
            
        result = agent.analyze_stock(symbol)
        print(agent.get_recommendation_summary(result))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()