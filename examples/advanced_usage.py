from stock_trading_agent import StockTradingAgent
from datetime import datetime
import json


def portfolio_analysis_example():
    """Example: Analyze an entire portfolio and get recommendations"""
    print("\n📊 PORTFOLIO ANALYSIS EXAMPLE")
    print("=" * 60)
    
    agent = StockTradingAgent()
    
    # Sample portfolio
    portfolio = {
        'AAPL': {'shares': 50, 'buy_price': 150.00},
        'GOOGL': {'shares': 20, 'buy_price': 2500.00},
        'TSLA': {'shares': 30, 'buy_price': 800.00},
        'MSFT': {'shares': 40, 'buy_price': 300.00}
    }
    
    portfolio_results = []
    total_current_value = 0
    total_initial_value = 0
    
    for symbol, holding in portfolio.items():
        print(f"\n🔍 Analyzing {symbol}...")
        result = agent.analyze_stock(symbol)
        
        if result['success']:
            current_value = result['current_price'] * holding['shares']
            initial_value = holding['buy_price'] * holding['shares']
            gain_loss = current_value - initial_value
            gain_loss_pct = (gain_loss / initial_value) * 100
            
            portfolio_results.append({
                'symbol': symbol,
                'shares': holding['shares'],
                'buy_price': holding['buy_price'],
                'current_price': result['current_price'],
                'current_value': current_value,
                'gain_loss': gain_loss,
                'gain_loss_pct': gain_loss_pct,
                'recommendation': result['recommendation'],
                'confidence': result['confidence']
            })
            
            total_current_value += current_value
            total_initial_value += initial_value
    
    # Print portfolio summary
    print("\n" + "=" * 60)
    print("📈 PORTFOLIO SUMMARY")
    print("=" * 60)
    
    for item in portfolio_results:
        emoji = "🟢" if item['gain_loss'] > 0 else "🔴"
        print(f"\n{item['symbol']}:")
        print(f"  Holdings: {item['shares']} shares")
        print(f"  Buy Price: ${item['buy_price']:.2f} → Current: ${item['current_price']:.2f}")
        print(f"  Position Value: ${item['current_value']:.2f}")
        print(f"  {emoji} P/L: ${item['gain_loss']:.2f} ({item['gain_loss_pct']:+.2f}%)")
        print(f"  📊 Recommendation: {item['recommendation']} (Confidence: {item['confidence']})")
    
    total_gain_loss = total_current_value - total_initial_value
    total_gain_loss_pct = (total_gain_loss / total_initial_value) * 100
    
    print("\n" + "-" * 60)
    print(f"💼 Total Portfolio Value: ${total_current_value:,.2f}")
    print(f"💰 Total Initial Investment: ${total_initial_value:,.2f}")
    emoji = "🟢" if total_gain_loss > 0 else "🔴"
    print(f"{emoji} Total P/L: ${total_gain_loss:,.2f} ({total_gain_loss_pct:+.2f}%)")
    print("=" * 60)


def sector_comparison_example():
    """Example: Compare stocks across different sectors"""
    print("\n🏭 SECTOR COMPARISON EXAMPLE")
    print("=" * 60)
    
    agent = StockTradingAgent()
    
    # Stocks from different sectors
    sectors = {
        'Technology': ['AAPL', 'MSFT', 'NVDA'],
        'Finance': ['JPM', 'BAC', 'GS'],
        'Healthcare': ['JNJ', 'PFE', 'UNH'],
        'Energy': ['XOM', 'CVX', 'COP']
    }
    
    sector_results = {}
    
    for sector, stocks in sectors.items():
        print(f"\n📊 Analyzing {sector} sector...")
        sector_data = []
        
        for symbol in stocks:
            result = agent.analyze_stock(symbol)
            if result['success']:
                sector_data.append({
                    'symbol': symbol,
                    'price': result['current_price'],
                    'recommendation': result['recommendation'],
                    'week_change': result['stock_data']['week_change'],
                    'month_change': result['stock_data']['month_change'],
                    'pe_ratio': result['stock_data']['pe_ratio']
                })
        
        sector_results[sector] = sector_data
    
    # Print sector comparison
    print("\n" + "=" * 60)
    print("📊 SECTOR PERFORMANCE COMPARISON")
    print("=" * 60)
    
    for sector, stocks in sector_results.items():
        print(f"\n{sector} Sector:")
        
        # Calculate sector averages
        avg_week_change = sum(s['week_change'] for s in stocks) / len(stocks)
        avg_month_change = sum(s['month_change'] for s in stocks) / len(stocks)
        buy_count = sum(1 for s in stocks if s['recommendation'] == 'BUY')
        
        print(f"  Average Week Change: {avg_week_change:+.2f}%")
        print(f"  Average Month Change: {avg_month_change:+.2f}%")
        print(f"  Buy Recommendations: {buy_count}/{len(stocks)}")
        
        print("\n  Individual Stocks:")
        for stock in stocks:
            print(f"    {stock['symbol']}: ${stock['price']:.2f} | "
                  f"Week: {stock['week_change']:+.2f}% | "
                  f"Rec: {stock['recommendation']}")


def momentum_scanner_example():
    """Example: Scan for stocks with strong momentum"""
    print("\n🚀 MOMENTUM SCANNER EXAMPLE")
    print("=" * 60)
    
    agent = StockTradingAgent()
    
    # List of stocks to scan
    watchlist = ['AAPL', 'GOOGL', 'TSLA', 'NVDA', 'META', 'AMZN', 'MSFT', 'NFLX', 'AMD', 'CRM']
    
    momentum_stocks = []
    
    print("Scanning for momentum stocks...")
    
    for symbol in watchlist:
        result = agent.analyze_stock(symbol)
        if result['success']:
            stock_data = result['stock_data']
            
            # Momentum criteria: positive week and month change
            if stock_data['week_change'] > 2 and stock_data['month_change'] > 5:
                momentum_stocks.append({
                    'symbol': symbol,
                    'company': stock_data['company_name'],
                    'price': stock_data['current_price'],
                    'week_change': stock_data['week_change'],
                    'month_change': stock_data['month_change'],
                    'volume_ratio': stock_data['volume'] / stock_data['avg_volume'],
                    'recommendation': result['recommendation']
                })
    
    # Sort by month change
    momentum_stocks.sort(key=lambda x: x['month_change'], reverse=True)
    
    print("\n🚀 TOP MOMENTUM STOCKS")
    print("=" * 60)
    
    for stock in momentum_stocks:
        volume_indicator = "📊" if stock['volume_ratio'] > 1.2 else "📉"
        print(f"\n{stock['symbol']} - {stock['company']}")
        print(f"  💵 Price: ${stock['price']:.2f}")
        print(f"  📈 Performance: Week +{stock['week_change']:.2f}% | Month +{stock['month_change']:.2f}%")
        print(f"  {volume_indicator} Volume: {stock['volume_ratio']:.2f}x average")
        print(f"  🎯 Recommendation: {stock['recommendation']}")


def value_screener_example():
    """Example: Screen for value stocks based on fundamentals"""
    print("\n💎 VALUE STOCK SCREENER EXAMPLE")
    print("=" * 60)
    
    agent = StockTradingAgent()
    
    # Value stocks to screen
    value_candidates = ['WMT', 'KO', 'JNJ', 'PG', 'VZ', 'T', 'IBM', 'INTC', 'CSCO', 'PFE']
    
    value_stocks = []
    
    print("Screening for value opportunities...")
    
    for symbol in value_candidates:
        result = agent.analyze_stock(symbol)
        if result['success']:
            data = result['stock_data']
            
            # Value criteria
            if (data['pe_ratio'] > 0 and data['pe_ratio'] < 20 and 
                data['dividend_yield'] > 0.02):
                
                value_stocks.append({
                    'symbol': symbol,
                    'company': data['company_name'],
                    'price': data['current_price'],
                    'pe_ratio': data['pe_ratio'],
                    'forward_pe': data['forward_pe'],
                    'dividend_yield': data['dividend_yield'] * 100,
                    'recommendation': result['recommendation'],
                    'beta': data['beta']
                })
    
    # Sort by P/E ratio
    value_stocks.sort(key=lambda x: x['pe_ratio'])
    
    print("\n💎 VALUE STOCK OPPORTUNITIES")
    print("=" * 60)
    
    for stock in value_stocks:
        risk = "Low Risk" if stock['beta'] < 1 else "Higher Risk"
        print(f"\n{stock['symbol']} - {stock['company']}")
        print(f"  💵 Price: ${stock['price']:.2f}")
        print(f"  📊 P/E Ratio: {stock['pe_ratio']:.2f} (Forward: {stock['forward_pe']:.2f})")
        print(f"  💰 Dividend Yield: {stock['dividend_yield']:.2f}%")
        print(f"  📈 Beta: {stock['beta']:.2f} ({risk})")
        print(f"  🎯 Recommendation: {stock['recommendation']}")


def export_analysis_example():
    """Example: Export analysis results to JSON"""
    print("\n📁 EXPORT ANALYSIS EXAMPLE")
    print("=" * 60)
    
    agent = StockTradingAgent()
    
    # Analyze multiple stocks and export
    stocks_to_analyze = ['AAPL', 'GOOGL', 'TSLA']
    analysis_results = []
    
    for symbol in stocks_to_analyze:
        print(f"Analyzing {symbol}...")
        result = agent.analyze_stock(symbol)
        if result['success']:
            analysis_results.append({
                'timestamp': datetime.now().isoformat(),
                'symbol': result['symbol'],
                'company_name': result['company_name'],
                'current_price': result['current_price'],
                'recommendation': result['recommendation'],
                'confidence': result['confidence'],
                'key_factors': result['key_factors'],
                'analysis_summary': result['analysis'][:500] + '...',  # First 500 chars
                'metrics': {
                    'week_change': result['stock_data']['week_change'],
                    'month_change': result['stock_data']['month_change'],
                    'pe_ratio': result['stock_data']['pe_ratio'],
                    'volume': result['stock_data']['volume'],
                    'market_cap': result['stock_data']['market_cap']
                }
            })
    
    # Export to JSON
    filename = f"stock_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\n✅ Analysis exported to {filename}")
    print(f"📊 Analyzed {len(analysis_results)} stocks")


if __name__ == "__main__":
    import sys
    
    examples = {
        '1': ('Portfolio Analysis', portfolio_analysis_example),
        '2': ('Sector Comparison', sector_comparison_example),
        '3': ('Momentum Scanner', momentum_scanner_example),
        '4': ('Value Screener', value_screener_example),
        '5': ('Export Analysis', export_analysis_example)
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in examples:
        name, func = examples[sys.argv[1]]
        print(f"\n🚀 Running {name} Example...")
        func()
    else:
        print("\n📚 Available Examples:")
        print("=" * 60)
        for key, (name, _) in examples.items():
            print(f"  {key}: {name}")
        print("\nUsage: python advanced_usage.py [example_number]")
        print("Example: python advanced_usage.py 1")
        
        # Run all examples
        print("\n🎯 Running all examples...")
        for name, func in examples.values():
            func()
            input("\nPress Enter to continue to next example...")