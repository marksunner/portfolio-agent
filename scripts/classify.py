#!/usr/bin/env python3
"""
Classification history manager for When→If tracking.
Usage: python3 classify.py <command> [args]

Commands:
  list                           - Show current classifications for all holdings
  history <SYMBOL>               - Show classification history for a symbol
  update <SYMBOL> <CLASS> <CATALYST> - Update classification (WHEN/TRANSITION/IF)
  alerts                         - Show recent transitions (last 30 days)
"""

import sys
import os
import json
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "classifications.json")

def load_data():
    """Load classification data"""
    if not os.path.exists(DATA_FILE):
        return {"_meta": {"description": "When→If classifications", "updated": "", "schema_version": "1.0"}}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save classification data"""
    data["_meta"]["updated"] = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def cmd_list():
    """List current classifications"""
    data = load_data()
    
    print("Current When→If Classifications:\n")
    
    # Group by classification
    by_class = {"WHEN": [], "TRANSITION": [], "IF": []}
    
    for symbol, history in data.items():
        if symbol.startswith("_"):
            continue
        if history:
            current = history[-1]["classification"]
            by_class.get(current, []).append(symbol)
    
    print("🟢 WHEN (timing debate only):")
    print(f"   {', '.join(sorted(by_class['WHEN'])) or 'None'}\n")
    
    print("🟡 TRANSITION (maximum uncertainty):")
    print(f"   {', '.join(sorted(by_class['TRANSITION'])) or 'None'}\n")
    
    print("🔴 IF (survival in question):")
    print(f"   {', '.join(sorted(by_class['IF'])) or 'None'}")

def cmd_history(symbol):
    """Show classification history for a symbol"""
    data = load_data()
    symbol = symbol.upper()
    
    if symbol not in data:
        print(f"No classification history for {symbol}")
        return
    
    print(f"Classification History for {symbol}:\n")
    
    for entry in data[symbol]:
        date = entry.get("date", "N/A")
        classification = entry.get("classification", "N/A")
        previous = entry.get("previous", None)
        catalyst = entry.get("catalyst", "N/A")
        
        emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(classification, "⚪")
        
        if previous:
            prev_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(previous, "⚪")
            print(f"[{date}] {prev_emoji} {previous} → {emoji} {classification}")
        else:
            print(f"[{date}] {emoji} {classification}")
        print(f"         Catalyst: {catalyst}\n")

def cmd_update(symbol, classification, catalyst):
    """Update classification for a symbol"""
    data = load_data()
    symbol = symbol.upper()
    classification = classification.upper()
    
    if classification not in ["WHEN", "TRANSITION", "IF"]:
        print(f"Invalid classification: {classification}")
        print("Must be one of: WHEN, TRANSITION, IF")
        return
    
    # Get previous classification
    previous = None
    if symbol in data and data[symbol]:
        previous = data[symbol][-1]["classification"]
        if previous == classification:
            print(f"{symbol} is already classified as {classification}")
            return
    
    # Create new entry
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "classification": classification,
        "catalyst": catalyst
    }
    if previous:
        entry["previous"] = previous
    
    # Add to history
    if symbol not in data:
        data[symbol] = []
    data[symbol].append(entry)
    
    save_data(data)
    
    emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(classification, "⚪")
    if previous:
        prev_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(previous, "⚪")
        print(f"Updated {symbol}: {prev_emoji} {previous} → {emoji} {classification}")
    else:
        print(f"Added {symbol}: {emoji} {classification}")
    print(f"Catalyst: {catalyst}")

def cmd_alerts():
    """Show recent classification changes"""
    data = load_data()
    cutoff = datetime.now() - timedelta(days=30)
    
    print("Recent Classification Changes (last 30 days):\n")
    
    changes = []
    for symbol, history in data.items():
        if symbol.startswith("_"):
            continue
        for entry in history:
            if "previous" in entry:
                try:
                    date = datetime.strptime(entry["date"], "%Y-%m-%d")
                    if date >= cutoff:
                        changes.append((date, symbol, entry))
                except:
                    pass
    
    if not changes:
        print("No classification changes in the last 30 days.")
        return
    
    # Sort by date descending
    changes.sort(key=lambda x: x[0], reverse=True)
    
    for date, symbol, entry in changes:
        prev = entry.get("previous", "?")
        curr = entry.get("classification", "?")
        catalyst = entry.get("catalyst", "N/A")
        
        prev_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(prev, "⚪")
        curr_emoji = {"WHEN": "🟢", "TRANSITION": "🟡", "IF": "🔴"}.get(curr, "⚪")
        
        # Flag critical transitions
        flag = ""
        if prev == "WHEN" and curr == "TRANSITION":
            flag = " ⚠️ ALERT"
        elif curr == "IF":
            flag = " 🚨 CRITICAL"
        
        print(f"[{entry['date']}] {symbol}: {prev_emoji} {prev} → {curr_emoji} {curr}{flag}")
        print(f"         {catalyst}\n")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "list":
        cmd_list()
    elif cmd == "history" and len(sys.argv) >= 3:
        cmd_history(sys.argv[2])
    elif cmd == "update" and len(sys.argv) >= 5:
        cmd_update(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    elif cmd == "alerts":
        cmd_alerts()
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
