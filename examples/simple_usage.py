from stock_trading_agent import StockTradingAgent


def single_stock_analysis():
    """Simple example: Analyze a single stock"""
    # Initialize the agent
    agent = StockTradingAgent()
    
    # Analyze Apple stock
    print("Analyzing Apple (AAPL)...")
    result = agent.analyze_stock('AAPL')
    
    # Check if analysis was successful
    if result['success']:
        print(f"\nStock: {result['company_name']} ({result['symbol']})")
        print(f"Current Price: ${result['current_price']}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Confidence: {result['confidence']}")
        print(f"\nKey Factors:")
        for factor in result['key_factors']:
            print(f"  - {factor}")
    else:
        print(f"Error: {result['error']}")


def quick_recommendation():
    """Get quick buy/sell recommendations for multiple stocks"""
    agent = StockTradingAgent()
    
    stocks = ['AAPL', 'GOOGL', 'TSLA', 'MSFT']
    
    print("Quick Stock Recommendations:")
    print("-" * 40)
    
    for symbol in stocks:
        result = agent.analyze_stock(symbol)
        if result['success']:
            emoji = {'BUY': '🟢', 'HOLD': '🟡', 'SELL': '🔴'}
            rec_emoji = emoji.get(result['recommendation'], '⚪')
            print(f"{symbol}: {rec_emoji} {result['recommendation']} @ ${result['current_price']}")
        else:
            print(f"{symbol}: ❌ Error analyzing stock")


def detailed_analysis():
    """Get detailed analysis with full report"""
    agent = StockTradingAgent()
    
    # Analyze Tesla
    result = agent.analyze_stock('TSLA')
    
    # Print full formatted report
    if result['success']:
        report = agent.get_recommendation_summary(result)
        print(report)
    else:
        print(f"Failed to analyze: {result['error']}")


def check_watchlist():
    """Check a watchlist of stocks"""
    agent = StockTradingAgent()
    
    # Your watchlist
    watchlist = {
        'Tech Giants': ['AAPL', 'GOOGL', 'MSFT'],
        'EV Stocks': ['TSLA', 'RIVN', 'LCID'],
        'Finance': ['JPM', 'BAC', 'GS']
    }
    
    for category, stocks in watchlist.items():
        print(f"\n{category}:")
        print("-" * 30)
        
        for symbol in stocks:
            result = agent.analyze_stock(symbol)
            if result['success']:
                # Show simplified info
                price_change = result['stock_data']['week_change']
                arrow = '↑' if price_change > 0 else '↓'
                color = '🟢' if result['recommendation'] == 'BUY' else '🟡' if result['recommendation'] == 'HOLD' else '🔴'
                
                print(f"{symbol}: ${result['current_price']:.2f} "
                      f"{arrow} {abs(price_change):.1f}% "
                      f"{color} {result['recommendation']}")


if __name__ == "__main__":
    print("=== Simple Stock Analysis Examples ===\n")
    
    print("1. Single Stock Analysis")
    print("-" * 40)
    single_stock_analysis()
    
    input("\nPress Enter to continue...")
    
    print("\n2. Quick Recommendations")
    print("-" * 40)
    quick_recommendation()
    
    input("\nPress Enter to continue...")
    
    print("\n3. Detailed Analysis Report")
    print("-" * 40)
    detailed_analysis()
    
    input("\nPress Enter to continue...")
    
    print("\n4. Watchlist Check")
    print("-" * 40)
    check_watchlist()