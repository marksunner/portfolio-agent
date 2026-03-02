#!/usr/bin/env python3
"""
Simple Finnhub API CLI wrapper for portfolio monitoring.
Usage: python3 finnhub-cli.py <command> [args]

Commands:
  quote <SYMBOL>              - Get current price
  quotes <SYM1,SYM2,...>      - Get multiple quotes
  news <SYMBOL>               - Get recent news
  profile <SYMBOL>            - Get company profile
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
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
