# Portfolio Agent Skill

## Purpose

Provides structured investment analysis for technology and AI-adjacent equities using a six-lens disruption framework. Integrates real-time market data with systematic risk assessment.

## When to Use

- User asks about stock/portfolio analysis
- Pre-market or post-market briefing requests
- Evaluating new investment opportunities
- Understanding why a position is moving
- Assessing AI disruption risk for a company

## Core Capabilities

### 1. Real-Time Data Access

```bash
# Get current quote
$SKILL_DIR/scripts/fh quote <SYMBOL>

# Multiple quotes
$SKILL_DIR/scripts/fh quotes <SYM1,SYM2,...>

# Company news
$SKILL_DIR/scripts/fh news <SYMBOL>

# Company profile
$SKILL_DIR/scripts/fh profile <SYMBOL>
```

**Requires:** Finnhub API key in `~/.config/finnhub/api_key`

### 2. Six-Lens Analysis Framework

Apply these lenses systematically when evaluating any position:

#### Lens 1: When→If Classifier
- **WHEN**: Market debates timing, not survival
- **IF**: Market questions if business survives
- **TRANSITION**: Maximum uncertainty zone

#### Lens 2: Three-Lever Repricing
- P/E compression
- Revenue multiple compression  
- WACC expansion

#### Lens 3: Tactical vs Structural
- Tactical = temporary (degrossing, risk-off)
- Structural = permanent (AI disruption, customer churn)

#### Lens 4: Jevons Paradox
- Supply-constrained → AI may expand demand
- Demand-constrained → AI compresses margins

#### Lens 5: Build-vs-Buy
- Can customers build this themselves with AI agents?
- High/Medium/Low vulnerability assessment

#### Lens 6: Survival Fitness
- Cash flow durability
- SBC discipline
- Balance sheet strength

### 3. Reporting Templates

#### Pre-Market Briefing
1. Scan overnight news for AI announcements
2. Check for When→If classification changes
3. Decompose pre-market moves (tactical vs structural)
4. Flag Jevons opportunities
5. Summarise with action recommendations

#### Post-Market Briefing
1. Decompose day's price action
2. Update Three-Lever assessments
3. Run Build-vs-Buy scan for new AI capabilities
4. Update Survival Fitness scores
5. Contrarian opportunity scan

## Sector Classifications

### Infrastructure (Low AI Disruption Risk)
- Data center cooling (VRT)
- Networking equipment (ANET)
- Connectors/cabling (APH, GLW)
- Power management (ETN)
- Power generation (CEG)
- Contract manufacturing (CLS)

### Compute (Medium Risk, Jevons Favorable)
- GPU cloud (CRWV)
- Semiconductors (NVDA)
- Optical components (LITE)

### SaaS (Higher Risk, Build-vs-Buy Vulnerable)
- Workflow automation tools
- Simple CRM/project management
- Reporting and dashboards

## Alert Thresholds

- **Price move >5%**: Immediate analysis required
- **When→If transition**: HIGH PRIORITY flag
- **AI capability announcement affecting holding**: Alert
- **Earnings/guidance news**: Full framework re-run

## Output Format

When providing analysis, structure as:

```markdown
## [SYMBOL] — Six-Lens Analysis

**When→If Classification:** [WHEN/IF/TRANSITION] [emoji]

**Three-Lever Assessment:**
- P/E: [value and trend]
- Revenue Multiple: [value and trend]
- WACC: [assessment]

**Tactical vs Structural:** [classification]
- [supporting evidence]

**Jevons Paradox:** [FAVORABLE/UNFAVORABLE/NEUTRAL]
- [reasoning]

**Build-vs-Buy Vulnerability:** [HIGH/MEDIUM/LOW]
- [reasoning]

**Survival Fitness:** [STRONG/ADEQUATE/CONCERNING/CRITICAL]
- FCF: [assessment]
- SBC: [assessment]
- Debt: [assessment]

**Overall Assessment:** [summary]
```

## Integration Notes

- This skill complements general web search for news
- Always cite data sources (Finnhub, news articles)
- For complex analysis, apply lenses sequentially
- Track classification changes over time in memory

## Files

- `scripts/fh` — Finnhub CLI wrapper
- `scripts/finnhub-cli.py` — Python API client
- `docs/` — Detailed lens documentation
- `examples/` — Sample analyses
