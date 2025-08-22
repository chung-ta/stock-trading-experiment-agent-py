from openai import OpenAI
from typing import Dict, Any
import json


class OpenAIStockAnalyzer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "OpenAI Stock Analyzer"
        
    def analyze_stock(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = self._create_analysis_prompt(stock_data)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert stock analyst. Provide detailed investment recommendations based on stock data. Always provide a clear BUY, HOLD, or SELL recommendation with detailed reasoning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            
            recommendation = "HOLD"
            if "BUY" in analysis.upper() and "SELL" not in analysis.upper()[:50]:
                recommendation = "BUY"
            elif "SELL" in analysis.upper() and "BUY" not in analysis.upper()[:50]:
                recommendation = "SELL"
            
            return {
                'success': True,
                'recommendation': recommendation,
                'analysis': analysis,
                'confidence': self._extract_confidence(analysis),
                'key_factors': self._extract_key_factors(stock_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'recommendation': 'ERROR',
                'analysis': f'Failed to analyze stock: {str(e)}'
            }
    
    def _create_analysis_prompt(self, stock_data: Dict[str, Any]) -> str:
        data = stock_data['data']
        
        prompt = f"""
        Analyze the following stock data for {data['company_name']} ({data['symbol']}) and provide an investment recommendation:
        
        Current Price: ${data['current_price']}
        Previous Close: ${data['previous_close']}
        
        Price Movement:
        - 1 Week Change: {data['week_change']}%
        - 1 Month Change: {data['month_change']}%
        - 52 Week Range: ${data['52_week_low']} - ${data['52_week_high']}
        
        Valuation Metrics:
        - P/E Ratio: {data['pe_ratio']}
        - Forward P/E: {data['forward_pe']}
        - EPS: ${data['earnings_per_share']}
        
        Trading Activity:
        - Volume: {data['volume']:,}
        - Average Volume: {data['avg_volume']:,}
        - Market Cap: ${data['market_cap']:,}
        
        Other Metrics:
        - Beta: {data['beta']}
        - Dividend Yield: {data['dividend_yield']}%
        - Sector: {data['sector']}
        - Industry: {data['industry']}
        - Current Analyst Rating: {data['recommendation']} (Score: {data['analyst_rating']})
        
        Please provide:
        1. A clear BUY, HOLD, or SELL recommendation
        2. Key reasons supporting your recommendation
        3. Risk factors to consider
        4. Price targets or entry/exit points if applicable
        5. Overall market sentiment and technical analysis
        
        Format your response as a comprehensive paragraph that flows naturally.
        """
        
        return prompt
    
    def _extract_confidence(self, analysis: str) -> str:
        analysis_lower = analysis.lower()
        
        if any(word in analysis_lower for word in ['strongly recommend', 'excellent', 'compelling', 'highly']):
            return "HIGH"
        elif any(word in analysis_lower for word in ['risky', 'cautious', 'uncertain', 'volatile']):
            return "LOW"
        else:
            return "MEDIUM"
    
    def _extract_key_factors(self, stock_data: Dict[str, Any]) -> list:
        data = stock_data['data']
        factors = []
        
        if data['week_change'] > 5:
            factors.append("Strong weekly momentum")
        elif data['week_change'] < -5:
            factors.append("Weak weekly performance")
            
        if data['pe_ratio'] > 0 and data['pe_ratio'] < 15:
            factors.append("Attractive P/E ratio")
        elif data['pe_ratio'] > 30:
            factors.append("High P/E ratio")
            
        if data['volume'] > data['avg_volume'] * 1.5:
            factors.append("High trading volume")
            
        if data['dividend_yield'] > 0.02:
            factors.append(f"Dividend yield: {data['dividend_yield']*100:.2f}%")
            
        current_price = data['current_price']
        week_52_high = data['52_week_high']
        week_52_low = data['52_week_low']
        
        if current_price >= week_52_high * 0.95:
            factors.append("Near 52-week high")
        elif current_price <= week_52_low * 1.05:
            factors.append("Near 52-week low")
            
        return factors