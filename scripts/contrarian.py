#!/usr/bin/env python3
"""
Contrarian opportunity scoring for tactical entry points.
Usage: python3 contrarian.py <command> [args]

Commands:
  score <SYMBOL> <DECLINE%> <TACTICAL|STRUCTURAL>  - Calculate contrarian score
  scan                                              - Scan portfolio for opportunities
  
The Contrarian Score formula:
  Score = Tactical Severity × Structural Soundness × Jevons Favorability

Where:
  - Tactical Severity = magnitude of recent decline attributed to tactical factors (0-10)
  - Structural Soundness = inverse of When→If risk (WHEN=3, TRANSITION=2, IF=1)
  - Jevons Favorability = supply constraint score (FAVORABLE=3, NEUTRAL=2, UNFAVORABLE=1)

Higher scores indicate more attractive contrarian opportunities.
"""

import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSIFICATIONS_FILE = os.path.join(SCRIPT_DIR, "..", "data", "classifications.json")

# Jevons assessments for portfolio (from framework analysis)
JEVONS = {
    "VRT": ("FAVORABLE", "Data center cooling demand grows with AI compute"),
    "ANET": ("FAVORABLE", "Network bandwidth demand grows with AI workloads"),
    "APH": ("FAVORABLE", "Physical connectors needed regardless of software efficiency"),
    "GLW": ("FAVORABLE", "Fiber demand grows with data transfer needs"),
    "CLS": ("FAVORABLE", "Manufacturing capacity needed for AI hardware"),
    "ETN": ("FAVORABLE", "Power management demand grows with data centers"),
    "CEG": ("FAVORABLE", "Nuclear power demand for 24/7 data center loads"),
    "LITE": ("FAVORABLE", "Optical components scale with bandwidth"),
    "NVDA": ("FAVORABLE", "GPU demand expands as AI capabilities prove out"),
    "CRWV": ("FAVORABLE", "GPU cloud demand expands with AI adoption"),
    "GOOGL": ("NEUTRAL", "Mixed - benefits from AI but also disrupted"),
    "AMZN": ("NEUTRAL", "Mixed - AWS benefits but retail at risk"),
    "NET": ("NEUTRAL", "Edge/CDN demand grows but Build-vs-Buy risk"),
    "RKLB": ("NEUTRAL", "Space launch separate from AI dynamics"),
}

def load_classifications():
    """Load current classifications"""
    if not os.path.exists(CLASSIFICATIONS_FILE):
        return {}
    with open(CLASSIFICATIONS_FILE, 'r') as f:
        data = json.load(f)
    return {k: v[-1]["classification"] for k, v in data.items() if not k.startswith("_") and v}

def calculate_score(symbol, decline_pct, move_type):
    """Calculate contrarian score"""
    classifications = load_classifications()
    
    symbol = symbol.upper()
    move_type = move_type.upper()
    
    # Tactical Severity (0-10 scale based on decline magnitude)
    # Only count if move is TACTICAL
    if move_type == "TACTICAL":
        tactical_severity = min(abs(decline_pct), 30) / 3  # Max 10 at 30% decline
    else:
        tactical_severity = 0  # Structural moves don't create contrarian opportunity
    
    # Structural Soundness (from When→If classification)
    classification = classifications.get(symbol, "TRANSITION")
    soundness_map = {"WHEN": 3, "TRANSITION": 2, "IF": 1}
    structural_soundness = soundness_map.get(classification, 2)
    
    # Jevons Favorability
    jevons, _ = JEVONS.get(symbol, ("NEUTRAL", "Unknown"))
    jevons_map = {"FAVORABLE": 3, "NEUTRAL": 2, "UNFAVORABLE": 1}
    jevons_score = jevons_map.get(jevons, 2)
    
    # Final score
    score = tactical_severity * structural_soundness * jevons_score
    
    return {
        "symbol": symbol,
        "decline_pct": decline_pct,
        "move_type": move_type,
        "tactical_severity": round(tactical_severity, 1),
        "classification": classification,
        "structural_soundness": structural_soundness,
        "jevons": jevons,
        "jevons_score": jevons_score,
        "contrarian_score": round(score, 1)
    }

def cmd_score(symbol, decline_pct, move_type):
    """Calculate and display contrarian score"""
    result = calculate_score(symbol, float(decline_pct), move_type)
    
    # Rating based on score
    score = result["contrarian_score"]
    if score >= 60:
        rating = "🟢 STRONG OPPORTUNITY"
    elif score >= 30:
        rating = "🟡 MODERATE OPPORTUNITY"
    elif score > 0:
        rating = "⚪ WEAK OPPORTUNITY"
    else:
        rating = "🔴 NOT CONTRARIAN (structural move)"
    
    print(f"Contrarian Analysis: {result['symbol']}\n")
    print("=" * 50)
    print(f"Recent Move: {result['decline_pct']}% ({result['move_type']})")
    print(f"\nComponents:")
    print(f"  Tactical Severity: {result['tactical_severity']}/10")
    print(f"  Structural Soundness: {result['structural_soundness']}/3 ({result['classification']})")
    print(f"  Jevons Favorability: {result['jevons_score']}/3 ({result['jevons']})")
    print(f"\n{'=' * 50}")
    print(f"CONTRARIAN SCORE: {score} / 90")
    print(f"Rating: {rating}")
    
    if score >= 30:
        print(f"\n💡 This could be an entry opportunity if:")
        print(f"   - The tactical selling appears to be exhausting")
        print(f"   - No new structural catalysts have emerged")
        print(f"   - Your position size allows for averaging down")

def cmd_scan():
    """Scan portfolio for contrarian opportunities (placeholder - needs price data)"""
    print("Portfolio Contrarian Scan\n")
    print("=" * 50)
    print("\nTo identify contrarian opportunities, I need:")
    print("  1. Recent price changes (from Finnhub quote data)")
    print("  2. Move classification (tactical vs structural)")
    print("\nRun individual scores with:")
    print("  contrarian.py score <SYMBOL> <DECLINE%> <TACTICAL|STRUCTURAL>")
    print("\nExample:")
    print("  contrarian.py score VRT -7 TACTICAL")
    print("\n(A full automated scan would integrate with fh quotes)")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "score" and len(sys.argv) >= 5:
        cmd_score(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "scan":
        cmd_scan()
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
