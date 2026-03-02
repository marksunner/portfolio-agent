#!/usr/bin/env python3
"""
Portfolio-level analysis for concentration and correlation risk.
Usage: python3 portfolio.py <command>

Commands:
  concentration    - Analyze sector concentration risk
  correlation      - Identify correlated catalyst exposure
  summary          - Full portfolio health summary
"""

import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSIFICATIONS_FILE = os.path.join(SCRIPT_DIR, "..", "data", "classifications.json")

# Sector definitions with thesis exposure
SECTORS = {
    "Data Center Infrastructure": {
        "symbols": ["VRT", "ANET", "APH", "GLW", "CLS", "ETN", "CEG", "LITE"],
        "thesis": "Data centers get built at scale",
        "risk_if_wrong": "Hyperscaler capex cuts, power grid constraints, policy/NIMBY opposition",
        "ai_disruption_risk": "LOW"
    },
    "Compute/GPU": {
        "symbols": ["NVDA", "CRWV"],
        "thesis": "AI training and inference demand grows exponentially",
        "risk_if_wrong": "Training efficiency gains reduce GPU demand, custom silicon displaces NVIDIA",
        "ai_disruption_risk": "MEDIUM"
    },
    "Cloud/Platform": {
        "symbols": ["GOOGL", "AMZN", "NET"],
        "thesis": "Cloud infrastructure remains essential for AI deployment",
        "risk_if_wrong": "On-prem inference, edge computing reduces cloud dependence",
        "ai_disruption_risk": "MEDIUM"
    },
    "Space": {
        "symbols": ["RKLB"],
        "thesis": "Commercial space launch market expands",
        "risk_if_wrong": "SpaceX dominance, launch demand plateau",
        "ai_disruption_risk": "LOW"
    }
}

def load_classifications():
    """Load current classifications"""
    if not os.path.exists(CLASSIFICATIONS_FILE):
        return {}
    with open(CLASSIFICATIONS_FILE, 'r') as f:
        data = json.load(f)
    return {k: v[-1]["classification"] for k, v in data.items() if not k.startswith("_") and v}

def cmd_concentration():
    """Analyze sector concentration"""
    classifications = load_classifications()
    
    print("📊 Portfolio Concentration Analysis\n")
    print("=" * 50)
    
    total_positions = sum(len(s["symbols"]) for s in SECTORS.values())
    
    for sector, info in SECTORS.items():
        symbols = info["symbols"]
        count = len(symbols)
        pct = (count / total_positions) * 100
        
        # Get classifications for this sector
        sector_class = [classifications.get(s, "?") for s in symbols]
        when_count = sector_class.count("WHEN")
        trans_count = sector_class.count("TRANSITION")
        if_count = sector_class.count("IF")
        
        print(f"\n{sector}")
        print(f"  Positions: {count} ({pct:.0f}% of portfolio)")
        print(f"  Holdings: {', '.join(symbols)}")
        print(f"  Classifications: 🟢{when_count} 🟡{trans_count} 🔴{if_count}")
        print(f"  AI Disruption Risk: {info['ai_disruption_risk']}")
        print(f"  Core Thesis: {info['thesis']}")
    
    # Calculate overall concentration
    infra = len(SECTORS["Data Center Infrastructure"]["symbols"])
    infra_pct = (infra / total_positions) * 100
    
    print("\n" + "=" * 50)
    print(f"\n⚠️  CONCENTRATION ALERT:")
    print(f"   Data Center Infrastructure = {infra_pct:.0f}% of portfolio")
    
    if infra_pct > 50:
        print(f"   HIGH concentration in single thesis")
        print(f"   Risk: If data center buildout slows, {infra} positions affected simultaneously")

def cmd_correlation():
    """Identify correlated catalyst exposure"""
    print("🔗 Correlated Catalyst Exposure\n")
    print("=" * 50)
    
    # Define correlated risk events
    correlations = [
        {
            "event": "Hyperscaler Capex Cut",
            "description": "Google/Microsoft/Amazon reduce data center spending",
            "affected": ["VRT", "ANET", "APH", "GLW", "CLS", "ETN", "LITE", "NVDA", "CRWV"],
            "severity": "HIGH"
        },
        {
            "event": "Power Grid Constraints",
            "description": "Utilities unable to deliver power to new data centers",
            "affected": ["VRT", "CEG", "ETN", "ANET", "CLS"],
            "severity": "MEDIUM"
        },
        {
            "event": "NIMBY/Policy Opposition",
            "description": "Local opposition blocks data center construction",
            "affected": ["VRT", "CEG", "ETN", "ANET", "CLS", "APH", "GLW"],
            "severity": "MEDIUM"
        },
        {
            "event": "AI Efficiency Breakthrough",
            "description": "10x training efficiency reduces compute demand",
            "affected": ["NVDA", "CRWV", "VRT", "ANET"],
            "severity": "HIGH"
        },
        {
            "event": "Custom Silicon Adoption",
            "description": "Hyperscalers move to in-house chips (TPU, Trainium)",
            "affected": ["NVDA", "CRWV"],
            "severity": "MEDIUM"
        },
        {
            "event": "AI Regulation",
            "description": "Significant AI compute restrictions enacted",
            "affected": ["NVDA", "CRWV", "GOOGL", "AMZN"],
            "severity": "MEDIUM"
        }
    ]
    
    for corr in correlations:
        print(f"\n📌 {corr['event']} ({corr['severity']} impact)")
        print(f"   Scenario: {corr['description']}")
        print(f"   Affected: {', '.join(corr['affected'])} ({len(corr['affected'])} positions)")
    
    print("\n" + "=" * 50)
    print("\n💡 HEDGING CONSIDERATIONS:")
    print("   - Portfolio is LONG data center buildout thesis")
    print("   - Consider: inverse positions, non-correlated assets, or smaller sizing")
    print("   - The 'picks and shovels' strategy has high internal correlation")

def cmd_summary():
    """Full portfolio health summary"""
    classifications = load_classifications()
    
    print("📈 Portfolio Health Summary")
    print("=" * 50)
    
    # Classification breakdown
    all_class = list(classifications.values())
    when_count = all_class.count("WHEN")
    trans_count = all_class.count("TRANSITION")
    if_count = all_class.count("IF")
    total = len(all_class)
    
    print(f"\n🎯 When→If Status:")
    print(f"   🟢 WHEN: {when_count}/{total} ({when_count/total*100:.0f}%)")
    print(f"   🟡 TRANSITION: {trans_count}/{total} ({trans_count/total*100:.0f}%)")
    print(f"   🔴 IF: {if_count}/{total} ({if_count/total*100:.0f}%)")
    
    if if_count > 0:
        if_symbols = [s for s, c in classifications.items() if c == "IF"]
        print(f"\n   ⚠️  IF positions requiring review: {', '.join(if_symbols)}")
    
    if trans_count > 0:
        trans_symbols = [s for s, c in classifications.items() if c == "TRANSITION"]
        print(f"\n   🔍 TRANSITION positions to monitor: {', '.join(trans_symbols)}")
    
    # Sector concentration
    print(f"\n📊 Sector Exposure:")
    total_positions = sum(len(s["symbols"]) for s in SECTORS.values())
    for sector, info in SECTORS.items():
        pct = (len(info["symbols"]) / total_positions) * 100
        print(f"   {sector}: {pct:.0f}%")
    
    # Top correlated risk
    print(f"\n⚠️  Highest Correlation Risk:")
    print(f"   'Hyperscaler Capex Cut' would affect 9 positions")
    print(f"   Consider this your primary tail risk scenario")
    
    # Overall assessment
    print(f"\n" + "=" * 50)
    health = "STRONG" if if_count == 0 and trans_count <= 2 else "MODERATE" if if_count <= 1 else "CONCERNING"
    emoji = "💪" if health == "STRONG" else "👀" if health == "MODERATE" else "⚠️"
    print(f"\n{emoji} Overall Portfolio Health: {health}")
    
    if health == "STRONG":
        print("   No IF positions, limited uncertainty")
    elif health == "MODERATE":
        print("   Some positions in transition - monitor closely")
    else:
        print("   Multiple concerning positions - review needed")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "concentration":
        cmd_concentration()
    elif cmd == "correlation":
        cmd_correlation()
    elif cmd == "summary":
        cmd_summary()
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
