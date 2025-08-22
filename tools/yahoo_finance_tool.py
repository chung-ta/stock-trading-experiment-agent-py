import yfinance as yf
from typing import Dict, Any
from datetime import datetime, timedelta
import time
import requests
import numpy as np


class YahooFinanceTool:
    def __init__(self):
        self.name = "Yahoo Finance Stock Data Fetcher"
        
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        try:
            # Use download method which is more reliable
            stock = yf.Ticker(symbol.upper())
            
            # Get basic price data using download method
            end_date = datetime.now()
            start_date = end_date - timedelta(days=35)
            
            # Download historical data with auto_adjust=True (new default)
            hist_data = yf.download(symbol.upper(), start=start_date, end=end_date, progress=False, auto_adjust=True)
            
            if hist_data.empty:
                return {
                    'success': False,
                    'error': 'No data available for this symbol',
                    'symbol': symbol,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Calculate current price and changes
            current_price = hist_data['Close'].iloc[-1].item()
            
            # Calculate week change
            week_ago_date = end_date - timedelta(days=7)
            week_data = hist_data[hist_data.index >= week_ago_date]
            week_change = 0
            if len(week_data) > 1:
                week_start_price = week_data['Close'].iloc[0].item()
                week_change = ((current_price - week_start_price) / week_start_price) * 100
            
            # Calculate month change
            month_change = 0
            if len(hist_data) > 1:
                month_start_price = hist_data['Close'].iloc[0].item()
                month_change = ((current_price - month_start_price) / month_start_price) * 100
            
            # Get today's data
            today_data = hist_data.iloc[-1]
            yesterday_data = hist_data.iloc[-2] if len(hist_data) > 1 else today_data
            
            # Try to get additional info, but don't fail if rate limited
            info = {}
            try:
                info = stock.info
            except:
                pass
            
            # Handle multi-column data properly
            def get_value(data, column):
                val = data[column]
                if hasattr(val, 'item'):
                    return val.item()
                elif isinstance(val, np.ndarray):
                    return float(val[0])
                else:
                    return float(val)
            
            stock_data = {
                'symbol': symbol.upper(),
                'company_name': info.get('longName', symbol.upper()),
                'current_price': round(current_price, 2),
                'previous_close': round(get_value(yesterday_data, 'Close'), 2),
                'open_price': round(get_value(today_data, 'Open'), 2),
                'day_high': round(get_value(today_data, 'High'), 2),
                'day_low': round(get_value(today_data, 'Low'), 2),
                'volume': int(get_value(today_data, 'Volume')),
                'avg_volume': int(hist_data['Volume'].values.mean()),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'week_change': round(week_change, 2),
                'month_change': round(month_change, 2),
                '52_week_high': round(float(hist_data['High'].values.max()), 2),
                '52_week_low': round(float(hist_data['Low'].values.min()), 2),
                'earnings_per_share': info.get('trailingEps', 0),
                'beta': info.get('beta', 0),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'recommendation': info.get('recommendationKey', 'N/A'),
                'analyst_rating': info.get('recommendationMean', 0)
            }
            
            return {
                'success': True,
                'data': stock_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'symbol': symbol,
                'timestamp': datetime.now().isoformat()
            }