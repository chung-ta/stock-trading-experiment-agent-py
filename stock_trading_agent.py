from typing import Dict, Any, Optional
from tools.yahoo_finance_tool import YahooFinanceTool
from tools.openai_analyzer import OpenAIStockAnalyzer
import os
from dotenv import load_dotenv


class StockTradingAgent:
    def __init__(self, openai_api_key: Optional[str] = None):
        load_dotenv()
        
        self.yahoo_tool = YahooFinanceTool()
        api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to the constructor.")
            
        self.analyzer = OpenAIStockAnalyzer(api_key)
        
    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        print(f"\n🔍 Analyzing {symbol.upper()}...")
        
        stock_data = self.yahoo_tool.get_stock_info(symbol)
        
        if not stock_data['success']:
            return {
                'success': False,
                'error': stock_data['error'],
                'message': f"Failed to fetch data for {symbol}: {stock_data['error']}"
            }
        
        print(f"✅ Retrieved stock data for {stock_data['data']['company_name']}")
        print(f"💰 Current Price: ${stock_data['data']['current_price']}")
        print(f"📊 Week Change: {stock_data['data']['week_change']}%")
        print(f"📈 Month Change: {stock_data['data']['month_change']}%")
        
        print("\n🤖 Analyzing with AI...")
        analysis = self.analyzer.analyze_stock(stock_data)
        
        if not analysis['success']:
            return {
                'success': False,
                'error': analysis['error'],
                'message': f"Failed to analyze stock: {analysis['error']}",
                'stock_data': stock_data['data']
            }
        
        return {
            'success': True,
            'symbol': symbol.upper(),
            'company_name': stock_data['data']['company_name'],
            'current_price': stock_data['data']['current_price'],
            'recommendation': analysis['recommendation'],
            'confidence': analysis['confidence'],
            'analysis': analysis['analysis'],
            'key_factors': analysis['key_factors'],
            'stock_data': stock_data['data']
        }
    
    def get_recommendation_summary(self, result: Dict[str, Any]) -> str:
        if not result['success']:
            return f"❌ Analysis failed: {result.get('error', 'Unknown error')}"
        
        emoji_map = {
            'BUY': '🟢',
            'HOLD': '🟡', 
            'SELL': '🔴'
        }
        
        recommendation_emoji = emoji_map.get(result['recommendation'], '⚪')
        
        summary = f"""
{'='*60}
📊 STOCK ANALYSIS REPORT
{'='*60}

🏢 Company: {result['company_name']} ({result['symbol']})
💵 Current Price: ${result['current_price']}

{recommendation_emoji} RECOMMENDATION: {result['recommendation']}
📊 Confidence Level: {result['confidence']}

🔑 Key Factors:
"""
        
        for factor in result['key_factors']:
            summary += f"  • {factor}\n"
        
        summary += f"""
📝 Detailed Analysis:
{'-'*60}
{result['analysis']}
{'-'*60}

⏰ Analysis Timestamp: {result['stock_data'].get('timestamp', 'N/A')}
{'='*60}
"""
        
        return summary