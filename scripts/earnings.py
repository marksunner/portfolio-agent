#!/usr/bin/env python3
"""
Earnings calendar integration for portfolio monitoring.
Usage: python3 earnings.py <command> [args]

Commands:
  upcoming [DAYS]           - Show upcoming earnings for portfolio (default: 14 days)
  check <SYMBOL>            - Check specific symbol's next earnings date
  alert                     - Show earnings within next 7 days (for alerting)
  week                      - This week's earnings calendar
"""

import sys
import os
import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSIFICATIONS_FILE = os.path.join(SCRIPT_DIR, "..", "data", "classifications.json")

API_KEY = os.environ.get("FINNHUB_API_KEY", "")
BASE_URL = "https://finnhub.io/api/v1"

# Portfolio symbols (could also be loaded from classifications.json)
PORTFOLIO = ["GOOGL", "AMZN", "APH", "ANET", "CLS", "NET", "CRWV", "GLW", "LITE", "NVDA", "RKLB", "VRT", "ETN", "CEG"]

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
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        print(f"API Error: {e.code} - {e.reason}", file=sys.stderr)
        return None

def load_classifications():
    """Load current classifications"""
    if not os.path.exists(CLASSIFICATIONS_FILE):
        return {}
    with open(CLASSIFICATIONS_FILE, 'r') as f:
        data = json.load(f)
    return {k: v[-1]["classification"] for k, v in data.items() if not k.startswith("_") and v}

def get_earnings_calendar(from_date, to_date):
    """Get earnings calendar for date range"""
    data = api_call("calendar/earnings", {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d")
    })
    return data.get("earningsCalendar", []) if data else []

def cmd_upcoming(days=14):
    """Show upcoming earnings for portfolio holdings"""
    classifications = load_classifications()
    
    today = datetime.now()
    end_date = today + timedelta(days=days)
    
    print(f"📅 Upcoming Earnings (next {days} days)\n")
    print("=" * 60)
    
    # Get earnings calendar
    calendar = get_earnings_calendar(today, end_date)
    
    # Filter for portfolio holdings
    portfolio_earnings = []
    for entry in calendar:
        symbol = entry.get("symbol", "")
        if symbol in PORTFOLIO:
            portfolio_earnings.append(entry)
    
    if not portfolio_earnings:
        print(f"\nNo portfolio holdings reporting in the next {days} days.")
        print(f"\nPortfolio tracked: {', '.join(PORTFOLIO)}")
        return
    
    # Sort by date
    portfolio_earnings.sort(key=lambda x: x.get("date", ""))
    
    for entry in portfolio_earnings:
        symbol = entry.get("symbol", "?")
        date = entry.get("date", "?")
        hour = entry.get("hour", "?")  # "bmo" (before market open) or "amc" (after market close)
        eps_estimate = entry.get("epsEstimate", "N/A")
        revenue_estimate = entry.get("revenueEstimate", "N/A")
        
        # Get classification
        classification = classifications.get(symbol, "?")
        class_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(classification, "⚪")
        
        # Format time
        time_str = "Pre-Market" if hour == "bmo" else "After-Close" if hour == "amc" else "TBD"
        
        # Days until
        try:
            earn_date = datetime.strptime(date, "%Y-%m-%d")
            days_until = (earn_date - today).days
            if days_until == 0:
                urgency = "🚨 TODAY"
            elif days_until == 1:
                urgency = "⚠️ TOMORROW"
            elif days_until <= 7:
                urgency = f"📢 {days_until} days"
            else:
                urgency = f"{days_until} days"
        except:
            urgency = "?"
        
        print(f"\n{class_emoji} {symbol} — {date} ({time_str}) — {urgency}")
        print(f"   Classification: {classification}")
        if eps_estimate != "N/A" and eps_estimate is not None:
            print(f"   EPS Estimate: ${eps_estimate}")
        if revenue_estimate != "N/A" and revenue_estimate is not None:
            rev_b = revenue_estimate / 1_000_000_000
            print(f"   Revenue Estimate: ${rev_b:.2f}B")
        
        # Flag risk for TRANSITION positions
        if classification == "TRANSITION":
            print(f"   ⚠️  TRANSITION position — earnings could trigger When→If shift")

def cmd_check(symbol):
    """Check next earnings date for a specific symbol"""
    symbol = symbol.upper()
    classifications = load_classifications()
    
    # Look ahead 90 days
    today = datetime.now()
    end_date = today + timedelta(days=90)
    
    calendar = get_earnings_calendar(today, end_date)
    
    for entry in calendar:
        if entry.get("symbol") == symbol:
            date = entry.get("date", "?")
            hour = entry.get("hour", "?")
            eps_estimate = entry.get("epsEstimate", "N/A")
            
            time_str = "Pre-Market" if hour == "bmo" else "After-Close" if hour == "amc" else "TBD"
            
            try:
                earn_date = datetime.strptime(date, "%Y-%m-%d")
                days_until = (earn_date - today).days
            except:
                days_until = "?"
            
            classification = classifications.get(symbol, "?")
            class_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(classification, "⚪")
            
            print(f"📅 {symbol} Next Earnings\n")
            print(f"   Date: {date} ({time_str})")
            print(f"   Days Until: {days_until}")
            print(f"   Classification: {class_emoji} {classification}")
            if eps_estimate != "N/A" and eps_estimate is not None:
                print(f"   EPS Estimate: ${eps_estimate}")
            
            if classification == "TRANSITION":
                print(f"\n   ⚠️  TRANSITION position — run full six-lens analysis before earnings")
            
            return
    
    print(f"No upcoming earnings found for {symbol} in the next 90 days.")

def cmd_alert():
    """Show earnings within next 7 days for alerting"""
    classifications = load_classifications()
    
    today = datetime.now()
    end_date = today + timedelta(days=7)
    
    calendar = get_earnings_calendar(today, end_date)
    
    # Filter for portfolio
    alerts = []
    for entry in calendar:
        symbol = entry.get("symbol", "")
        if symbol in PORTFOLIO:
            alerts.append(entry)
    
    if not alerts:
        print("✅ No portfolio earnings in the next 7 days.")
        return
    
    alerts.sort(key=lambda x: x.get("date", ""))
    
    print("🚨 EARNINGS ALERTS (Next 7 Days)\n")
    print("=" * 50)
    
    for entry in alerts:
        symbol = entry.get("symbol", "?")
        date = entry.get("date", "?")
        hour = entry.get("hour", "?")
        
        classification = classifications.get(symbol, "?")
        class_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(classification, "⚪")
        
        time_str = "Pre-Market" if hour == "bmo" else "After-Close" if hour == "amc" else "TBD"
        
        try:
            earn_date = datetime.strptime(date, "%Y-%m-%d")
            days_until = (earn_date - today).days
            if days_until == 0:
                urgency = "🚨 TODAY"
            elif days_until == 1:
                urgency = "⚠️ TOMORROW"
            else:
                urgency = f"{days_until} days"
        except:
            urgency = "?"
        
        risk_flag = " ← REVIEW NEEDED" if classification in ["TRANSITION", "IF"] else ""
        
        print(f"{class_emoji} {symbol}: {date} ({time_str}) — {urgency}{risk_flag}")

def cmd_week():
    """Show this week's earnings"""
    today = datetime.now()
    # Find Monday of this week
    monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)
    
    print(f"📅 This Week's Earnings ({monday.strftime('%b %d')} - {friday.strftime('%b %d')})\n")
    print("=" * 50)
    
    calendar = get_earnings_calendar(monday, friday)
    
    # Filter for portfolio
    week_earnings = [e for e in calendar if e.get("symbol") in PORTFOLIO]
    
    if not week_earnings:
        print("\nNo portfolio holdings reporting this week.")
        return
    
    # Group by day
    by_day = {}
    for entry in week_earnings:
        date = entry.get("date", "Unknown")
        if date not in by_day:
            by_day[date] = []
        by_day[date].append(entry)
    
    classifications = load_classifications()
    
    for date in sorted(by_day.keys()):
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            day_name = dt.strftime("%A")
        except:
            day_name = "Unknown"
        
        print(f"\n{day_name} ({date}):")
        for entry in by_day[date]:
            symbol = entry.get("symbol", "?")
            hour = entry.get("hour", "?")
            time_str = "BMO" if hour == "bmo" else "AMC" if hour == "amc" else "?"
            
            classification = classifications.get(symbol, "?")
            class_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(classification, "⚪")
            
            print(f"   {class_emoji} {symbol} ({time_str})")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "upcoming":
        days = int(sys.argv[2]) if len(sys.argv) >= 3 else 14
        cmd_upcoming(days)
    elif cmd == "check" and len(sys.argv) >= 3:
        cmd_check(sys.argv[2])
    elif cmd == "alert":
        cmd_alert()
    elif cmd == "week":
        cmd_week()
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
