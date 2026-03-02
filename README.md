# Portfolio Agent

![Version](https://img.shields.io/badge/version-1.1.0-blue)

**An AI-powered investment analysis framework for OpenClaw agents.**

Portfolio Agent provides a structured analytical methodology for evaluating technology and AI-adjacent equities through the lens of disruption risk and opportunity. Designed for use by AI agents providing portfolio monitoring and investment intelligence.

[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://github.com/openclaw/openclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

The AI revolution has fundamentally changed how technology companies should be evaluated. Traditional metrics (P/E ratios, revenue growth, net dollar retention) remain important but insufficient. Portfolio Agent adds a structured disruption analysis layer that helps identify:

- **When→If Transitions**: Companies shifting from "when will disruption arrive?" to "will the business survive?"
- **Tactical vs Structural Moves**: Distinguishing hedge fund degrossing from genuine fundamental reassessment
- **Jevons Paradox Opportunities**: Sectors where AI may expand demand rather than destroy it
- **Build-vs-Buy Vulnerabilities**: Companies exposed to customers building their own AI-powered alternatives
- **Survival Fitness**: Balance sheet resilience to weather multi-year AI transition uncertainty

## Features

- 📊 **Six-Lens Analysis Framework** — Structured methodology for comprehensive equity evaluation
- 📈 **Real-Time Data Integration** — Finnhub API integration for live quotes, news, financials, and analyst recommendations
- 🔔 **Automated Alerting** — Configurable thresholds for price moves, news events, and classification changes
- 📝 **Structured Reporting** — Pre-market and post-market briefing templates
- 🎯 **Contrarian Scoring** — Formula-based identification of tactical overselling opportunities
- 📋 **Classification History** — Track When→If transitions over time with catalysts
- 🔗 **Portfolio-Level Analysis** — Concentration risk and correlated catalyst exposure mapping
- ⚡ **Lens Interaction Patterns** — Named patterns like "Right Thesis, Wrong Vehicle" for deeper insight
- 🔍 **Narrative Detection** — Distinguish genuine catalysts from amplified narratives

## The Six Analytical Lenses

### 1. When→If Disruption Classifier

Categorises market sentiment toward a company's cash flow durability:

| Classification | Description | Risk Level |
|----------------|-------------|------------|
| **WHEN** | Market debates timing of disruption, not survival | Standard |
| **IF** | Market questions whether business model survives | Elevated |
| **TRANSITION** | Active shift from WHEN to IF — maximum uncertainty | Critical |

### 2. Three-Lever Repricing Model

Decomposes valuation changes into three mechanisms:
- **P/E Compression** — Higher yield demanded for holding the equity
- **Revenue Multiple Compression** — Reduced confidence in future growth
- **WACC Expansion** — Higher discount rate for future cash flows

### 3. Tactical vs Structural Decomposition

Distinguishes temporary from permanent price pressure:
- **Tactical**: Hedge fund degrossing, broad risk-off, no company-specific catalyst
- **Structural**: AI capability announcements, customer churn data, competitive threats

### 4. Jevons Paradox Test

Evaluates whether AI-driven cost reduction might paradoxically *increase* demand:
- Supply-constrained markets → Jevons likely → Potential beneficiary
- Demand-constrained markets → Jevons unlikely → Disruption risk

### 5. Build-vs-Buy Power Shift

Assesses vulnerability to customers building AI-powered alternatives:
- **High Vulnerability**: Workflow automation, simple CRM, reporting tools
- **Medium Vulnerability**: Complex analytics, compliance tools with data moats
- **Low Vulnerability**: Infrastructure, platforms with network effects, mission-critical systems

### 6. Cash Flow Durability & Survival Fitness

Evaluates financial resilience for the AI transition:
- Free cash flow as % of revenue
- Stock-based compensation discipline
- Debt-to-equity and refinancing timeline
- Strategic AI positioning

## Installation

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured
- Python 3.9+ for data integration scripts
- Finnhub API key (free tier: 60 calls/minute)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/marksunner/portfolio-agent.git
cd portfolio-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API credentials:**
```bash
mkdir -p ~/.config/finnhub
echo "YOUR_FINNHUB_API_KEY" > ~/.config/finnhub/api_key
chmod 600 ~/.config/finnhub/api_key
```

4. **Add to OpenClaw skills directory:**
```bash
cp -r . /path/to/openclaw/skills/portfolio-agent/
```

## Usage

### Market Data Commands

```bash
# Get real-time quote
./scripts/fh quote NVDA

# Multiple quotes
./scripts/fh quotes GOOGL,AMZN,VRT,ANET

# Company news
./scripts/fh news VRT

# Company profile
./scripts/fh profile ANET

# Financial metrics (P/E, FCF, margins, debt)
./scripts/fh financials VRT

# Earnings history with surprises
./scripts/fh earnings NVDA

# Analyst recommendations and sentiment trend
./scripts/fh recommendations ANET

# Peer companies for relative valuation
./scripts/fh peers GOOGL
```

### Classification Tracking

```bash
# List current When→If classifications
./scripts/classify.py list

# View history for a symbol
./scripts/classify.py history CRWV

# Update classification with catalyst
./scripts/classify.py update CRWV IF "Q4 losses worse than expected, lawsuit filed"

# Show recent transitions (last 30 days)
./scripts/classify.py alerts
```

### Portfolio Analysis

```bash
# Sector concentration risk
./scripts/portfolio.py concentration

# Correlated catalyst exposure
./scripts/portfolio.py correlation

# Full portfolio health summary
./scripts/portfolio.py summary
```

### Contrarian Scoring

```bash
# Calculate contrarian score for a tactical dip
# Formula: Tactical Severity × Structural Soundness × Jevons Favorability
./scripts/contrarian.py score VRT -15 TACTICAL

# Score 60+ = strong, 30-60 = moderate, <30 = weak
# Structural moves score 0 (not contrarian)
```

### Earnings Calendar

```bash
# Upcoming earnings for portfolio holdings
./scripts/earnings.py upcoming 14

# Check specific symbol
./scripts/earnings.py check NVDA

# 7-day alert (for pre-market check)
./scripts/earnings.py alert
```

### Agent Integration

Add to your OpenClaw configuration to enable automated portfolio monitoring:

```yaml
skills:
  - name: portfolio-agent
    path: ./skills/portfolio-agent
```

The agent can then:
- Run scheduled pre-market and post-market analyses
- Alert on significant price moves or news
- Apply the six-lens framework to evaluate positions
- Track When→If classification changes over time

### Example Analysis Output

```markdown
## CRWV (CoreWeave) — Six-Lens Analysis

**When→If Classification:** TRANSITION ⚠️
- Recent shift from WHEN to IF territory
- Catalyst: $30B capex guidance, widening losses, class action lawsuit

**Three-Lever Assessment:**
- P/E: N/A (negative earnings)
- Revenue Multiple: Compressed from 15x to 8x ARR
- WACC: Elevated due to balance sheet concerns

**Tactical vs Structural:** STRUCTURAL
- Company-specific catalyst (earnings, lawsuit)
- Not correlated with broader market degrossing

**Jevons Paradox:** FAVORABLE
- AI compute is supply-constrained
- Demand likely to expand faster than commoditisation

**Build-vs-Buy Vulnerability:** LOW
- GPU cloud infrastructure cannot be DIY'd
- Physical compute moat intact

**Survival Fitness:** CONCERNING
- FCF: Negative (heavy investment phase)
- SBC: Elevated
- Debt: Rising significantly
- Cash runway: Adequate if financing continues

**Overall Assessment:** HIGH RISK / HIGH REWARD
- Structural concerns are real (balance sheet, execution)
- But Jevons Paradox suggests demand thesis intact
- Position sizing should reflect uncertainty
```

## Configuration

### Portfolio Definition

Create a `portfolio.yaml` file:

```yaml
portfolio:
  name: "AI Infrastructure Portfolio"
  holdings:
    - symbol: VRT
      category: infrastructure
      thesis: "Data center cooling leader"
    - symbol: ANET
      category: infrastructure  
      thesis: "High-speed networking for AI clusters"
    - symbol: CRWV
      category: compute
      thesis: "GPU cloud for AI workloads"
      
  watchlist:
    - symbol: ETN
      interest: "Power management infrastructure"
    - symbol: CEG
      interest: "Nuclear power for data centers"

alerts:
  price_threshold_pct: 5
  news_keywords:
    - "AI"
    - "data center"
    - "earnings"
```

### Cron Integration

For automated monitoring, add to your OpenClaw cron configuration:

```yaml
cron:
  - name: "Pre-Market Briefing"
    schedule: "30 13 * * 1-5"  # 1:30 PM GMT (before US open)
    task: "Run pre-market portfolio analysis using six-lens framework"
    
  - name: "Post-Market Briefing"  
    schedule: "30 21 * * 1-5"  # 9:30 PM GMT (after US close)
    task: "Run post-market portfolio analysis with price decomposition"
```

## Framework Deep Dive

For detailed documentation on each analytical lens, see:

- [docs/when-if-classifier.md](docs/when-if-classifier.md)
- [docs/three-lever-model.md](docs/three-lever-model.md)
- [docs/tactical-structural.md](docs/tactical-structural.md)
- [docs/jevons-paradox.md](docs/jevons-paradox.md)
- [docs/build-vs-buy.md](docs/build-vs-buy.md)
- [docs/survival-fitness.md](docs/survival-fitness.md)

## Contributing

Contributions are welcome! Areas of particular interest:

- Additional data source integrations (Alpha Vantage, Yahoo Finance)
- Enhanced Jevons Paradox sector mappings
- Historical backtesting of When→If transitions
- Improved survival fitness scoring algorithms

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

Framework methodology derived from investment analysis principles discussed on the [All-In Podcast](https://www.allinpodcast.co/), systematised and enhanced for automated portfolio analysis.

---

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — AI agents for everyone.*
