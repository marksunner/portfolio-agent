#!/usr/bin/env python3
"""
Simple Finnhub API CLI wrapper for portfolio monitoring.
Usage: python3 finnhub-cli.py <command> [args]

Commands:
  quote <SYMBOL>              - Get current price
  quotes <SYM1,SYM2,...>      - Get multiple quotes
  news <SYMBOL>               - Get recent news
  profile <SYMBOL>            - Get company profile
  financials <SYMBOL>         - Get key financial metrics (P/E, FCF, margins)
  earnings <SYMBOL>           - Get recent earnings history
  recommendations <SYMBOL>    - Get analyst recommendations
  peers <SYMBOL>              - Get peer companies
"""

import sys
import os
import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import datetime, timedelta

API_KEY = os.environ.get("FINNHUB_API_KEY", "")
BASE_URL = "https://finnhub.io/api/v1"

def api_call(endpoint, params=None):
    """Make API call to Finnhub"""
    if not API_KEY:
        print("Error: FINNHUB_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    url = f"{BASE_URL}/{endpoint}?token={API_KEY}"
    if params:
        for k, v in params.items():
            url += f"&{k}={v}"
    
    try:
        req = Request(url, headers={"User-Agent": "finnhub-cli/1.0"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        print(f"API Error: {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)

def cmd_quote(symbol):
    """Get current quote for a symbol"""
    data = api_call("quote", {"symbol": symbol.upper()})
    if data.get("c", 0) == 0:
        print(f"No data for {symbol}")
        return
    
    change_pct = ((data["c"] - data["pc"]) / data["pc"] * 100) if data["pc"] else 0
    direction = "🟢" if change_pct >= 0 else "🔴"
    
    print(f"{symbol.upper()}: ${data['c']:.2f} {direction} {change_pct:+.2f}%")
    print(f"  Open: ${data['o']:.2f} | High: ${data['h']:.2f} | Low: ${data['l']:.2f}")
    print(f"  Previous Close: ${data['pc']:.2f}")

def cmd_quotes(symbols):
    """Get quotes for multiple symbols"""
    for symbol in symbols.split(","):
        symbol = symbol.strip().upper()
        if not symbol:
            continue
        data = api_call("quote", {"symbol": symbol})
        if data.get("c", 0) == 0:
            print(f"{symbol}: No data")
            continue
        
        change_pct = ((data["c"] - data["pc"]) / data["pc"] * 100) if data["pc"] else 0
        direction = "🟢" if change_pct >= 0 else "🔴"
        print(f"{symbol}: ${data['c']:.2f} {direction} {change_pct:+.2f}%")

def cmd_news(symbol):
    """Get recent news for a symbol"""
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    data = api_call("company-news", {
        "symbol": symbol.upper(),
        "from": week_ago.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d")
    })
    
    if not data:
        print(f"No recent news for {symbol}")
        return
    
    print(f"Recent news for {symbol.upper()}:\n")
    for item in data[:5]:  # Top 5 stories
        dt = datetime.fromtimestamp(item.get("datetime", 0))
        print(f"[{dt.strftime('%Y-%m-%d')}] {item.get('headline', 'No headline')}")
        print(f"  Source: {item.get('source', 'Unknown')}")
        if item.get("summary"):
            summary = item["summary"][:200] + "..." if len(item.get("summary", "")) > 200 else item.get("summary", "")
            print(f"  {summary}")
        print()

def cmd_profile(symbol):
    """Get company profile"""
    data = api_call("stock/profile2", {"symbol": symbol.upper()})
    
    if not data:
        print(f"No profile data for {symbol}")
        return
    
    print(f"{data.get('name', symbol.upper())} ({data.get('ticker', symbol.upper())})")
    print(f"  Industry: {data.get('finnhubIndustry', 'N/A')}")
    print(f"  Market Cap: ${data.get('marketCapitalization', 0):,.0f}M")
    print(f"  Exchange: {data.get('exchange', 'N/A')}")
    print(f"  IPO: {data.get('ipo', 'N/A')}")
    print(f"  Website: {data.get('weburl', 'N/A')}")

def cmd_financials(symbol):
    """Get key financial metrics for Three-Lever and Survival Fitness analysis"""
    data = api_call("stock/metric", {"symbol": symbol.upper(), "metric": "all"})
    
    if not data or not data.get("metric"):
        print(f"No financial data for {symbol}")
        return
    
    m = data["metric"]
    symbol = symbol.upper()
    
    print(f"Financial Metrics for {symbol}:\n")
    
    # Valuation (Three-Lever: P/E, Revenue Multiple)
    print("📊 Valuation:")
    print(f"  P/E (TTM): {m.get('peBasicExclExtraTTM', 'N/A')}")
    print(f"  P/E (NTM): {m.get('peNormalizedAnnual', 'N/A')}")
    print(f"  P/S (TTM): {m.get('psTTM', 'N/A')}")
    print(f"  EV/Revenue: {m.get('enterpriseValueOverEBITDATTM', 'N/A')}")
    print(f"  EV/EBITDA: {m.get('evToEbitda', 'N/A')}")
    
    # Profitability (Survival Fitness)
    print("\n💰 Profitability:")
    print(f"  Gross Margin: {m.get('grossMarginTTM', 'N/A')}%")
    print(f"  Operating Margin: {m.get('operatingMarginTTM', 'N/A')}%")
    print(f"  Net Margin: {m.get('netProfitMarginTTM', 'N/A')}%")
    print(f"  ROE: {m.get('roeTTM', 'N/A')}%")
    print(f"  ROA: {m.get('roaTTM', 'N/A')}%")
    
    # Cash Flow (Survival Fitness: FCF)
    print("\n🏦 Cash Flow:")
    print(f"  FCF Yield: {m.get('freeCashFlowYieldTTM', 'N/A')}%")
    print(f"  FCF/Share: ${m.get('freeCashFlowPerShareTTM', 'N/A')}")
    print(f"  Cash/Share: ${m.get('cashPerShareTTM', 'N/A')}")
    
    # Balance Sheet (Survival Fitness: Debt)
    print("\n📋 Balance Sheet:")
    print(f"  Current Ratio: {m.get('currentRatioQuarterly', 'N/A')}")
    print(f"  Debt/Equity: {m.get('totalDebtToEquityQuarterly', 'N/A')}")
    print(f"  LT Debt/Equity: {m.get('longTermDebtToEquityQuarterly', 'N/A')}")
    
    # Growth
    print("\n📈 Growth:")
    print(f"  Revenue Growth (YoY): {m.get('revenueGrowthTTMYoy', 'N/A')}%")
    print(f"  EPS Growth (YoY): {m.get('epsGrowthTTMYoy', 'N/A')}%")

def cmd_earnings(symbol):
    """Get recent earnings history"""
    data = api_call("stock/earnings", {"symbol": symbol.upper()})
    
    if not data:
        print(f"No earnings data for {symbol}")
        return
    
    print(f"Earnings History for {symbol.upper()}:\n")
    
    for item in data[:4]:  # Last 4 quarters
        period = item.get("period", "N/A")
        actual = item.get("actual", "N/A")
        estimate = item.get("estimate", "N/A")
        
        if actual != "N/A" and estimate != "N/A" and estimate != 0:
            surprise_pct = ((actual - estimate) / abs(estimate)) * 100
            surprise_emoji = "✅" if surprise_pct >= 0 else "❌"
            surprise_str = f"{surprise_emoji} {surprise_pct:+.1f}%"
        else:
            surprise_str = "N/A"
        
        print(f"Q ending {period}:")
        print(f"  EPS Actual: ${actual} | Estimate: ${estimate} | Surprise: {surprise_str}")

def cmd_recommendations(symbol):
    """Get analyst recommendations"""
    data = api_call("stock/recommendation", {"symbol": symbol.upper()})
    
    if not data:
        print(f"No recommendation data for {symbol}")
        return
    
    print(f"Analyst Recommendations for {symbol.upper()}:\n")
    
    # Most recent period
    if data:
        latest = data[0]
        period = latest.get("period", "N/A")
        print(f"Period: {period}")
        print(f"  Strong Buy: {latest.get('strongBuy', 0)}")
        print(f"  Buy: {latest.get('buy', 0)}")
        print(f"  Hold: {latest.get('hold', 0)}")
        print(f"  Sell: {latest.get('sell', 0)}")
        print(f"  Strong Sell: {latest.get('strongSell', 0)}")
        
        # Calculate sentiment
        total = sum([latest.get('strongBuy', 0), latest.get('buy', 0), 
                     latest.get('hold', 0), latest.get('sell', 0), latest.get('strongSell', 0)])
        if total > 0:
            bullish = latest.get('strongBuy', 0) + latest.get('buy', 0)
            bearish = latest.get('sell', 0) + latest.get('strongSell', 0)
            bull_pct = (bullish / total) * 100
            print(f"\n  Sentiment: {bull_pct:.0f}% Bullish")
        
        # Trend check - compare to 3 months ago if available
        if len(data) >= 3:
            old = data[2]
            old_bullish = old.get('strongBuy', 0) + old.get('buy', 0)
            new_bullish = latest.get('strongBuy', 0) + latest.get('buy', 0)
            if new_bullish > old_bullish:
                print("  Trend: 📈 Improving")
            elif new_bullish < old_bullish:
                print("  Trend: 📉 Declining")
            else:
                print("  Trend: ➡️ Stable")

def cmd_peers(symbol):
    """Get peer companies for relative valuation"""
    data = api_call("stock/peers", {"symbol": symbol.upper()})
    
    if not data:
        print(f"No peer data for {symbol}")
        return
    
    print(f"Peer Companies for {symbol.upper()}:\n")
    print(", ".join(data[:10]))  # Top 10 peers

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "quote" and len(sys.argv) >= 3:
        cmd_quote(sys.argv[2])
    elif cmd == "quotes" and len(sys.argv) >= 3:
        cmd_quotes(sys.argv[2])
    elif cmd == "news" and len(sys.argv) >= 3:
        cmd_news(sys.argv[2])
    elif cmd == "profile" and len(sys.argv) >= 3:
        cmd_profile(sys.argv[2])
    elif cmd == "financials" and len(sys.argv) >= 3:
        cmd_financials(sys.argv[2])
    elif cmd == "earnings" and len(sys.argv) >= 3:
        cmd_earnings(sys.argv[2])
    elif cmd == "recommendations" and len(sys.argv) >= 3:
        cmd_recommendations(sys.argv[2])
    elif cmd == "peers" and len(sys.argv) >= 3:
        cmd_peers(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
