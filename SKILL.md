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

# Financial metrics (P/E, FCF, margins, debt) - for Three-Lever & Survival
$SKILL_DIR/scripts/fh financials <SYMBOL>

# Earnings history
$SKILL_DIR/scripts/fh earnings <SYMBOL>

# Analyst recommendations - for sentiment shifts
$SKILL_DIR/scripts/fh recommendations <SYMBOL>

# Peer companies - for relative valuation
$SKILL_DIR/scripts/fh peers <SYMBOL>
```

**Requires:** Finnhub API key in `~/.config/finnhub/api_key`

**Rate Limits (Free Tier):** 60 calls/minute
- Priority 1: Quote + News for all holdings (always run)
- Priority 2: Full analysis for flagged positions (run when triggered)
- Priority 3: Deep dive with all endpoints (on demand or weekly)
- Add 1-second delay between calls to stay within limits

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

**Narrative Check:** When identifying a company-specific catalyst, verify:
1. **Source credibility** — Reputable analyst, earnings report, or unverified blog?
2. **Author incentives** — Does the author have positions in named stocks?
3. **Analytical substance** — Verifiable financial analysis or scenario fiction?
4. **Propagation pattern** — Organic engagement or amplified by interested parties?

If a catalyst fails multiple checks, classify as **NARRATIVE-DRIVEN** rather than STRUCTURAL.

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

### 3. Lens Interaction Patterns ⚡

**The framework's power comes from how lenses interact.** Don't just list assessments — identify these patterns:

#### Pattern 1: "Right Thesis, Wrong Vehicle"
- Jevons = FAVORABLE + Survival Fitness = CONCERNING
- The sector will grow, but this company may not survive to benefit
- **Action:** Consider stronger competitor in same space

#### Pattern 2: "Tactical Opportunity in Structural Uncertainty"
- When→If = TRANSITION + Tactical vs Structural = TACTICAL
- Stock sold for temporary reasons while existential question unresolved
- **Action:** Potential entry IF you believe TRANSITION resolves back to WHEN

#### Pattern 3: "Moat Under Siege"
- Build-vs-Buy = MEDIUM/HIGH + Survival Fitness = STRONG
- Has balance sheet to fight but competitive position eroding
- **Action:** Watch net dollar retention and customer renewals obsessively

#### Pattern 4: "Fortress Position"
- When→If = WHEN + Jevons = FAVORABLE + Build-vs-Buy = LOW + Survival = STRONG
- All lenses aligned positively — core holding
- **Action:** Size accordingly; add on tactical dips

#### Pattern 5: "Narrative vs Reality"
- When→If suddenly shifts to TRANSITION + no change in Three-Lever fundamentals
- Market reacting to narrative (viral article, demo) not financial reality
- **Action:** Check if narrative catalyst has genuine analytical substance

### 4. Reporting Templates

#### Pre-Market Briefing
1. Scan overnight news for AI announcements
2. Check for When→If classification changes
3. Decompose pre-market moves (tactical vs structural)
4. Flag Jevons opportunities
5. Identify lens interaction patterns
6. Summarise with action recommendations

#### Post-Market Briefing
1. Decompose day's price action
2. Update Three-Lever assessments
3. Run Build-vs-Buy scan for new AI capabilities
4. Update Survival Fitness scores
5. Contrarian opportunity scan
6. Note any pattern changes (e.g., "Right Thesis, Wrong Vehicle" emerging)

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
- **Pattern change**: Flag when lens interactions shift (e.g., Survival degrades from STRONG to CONCERNING)

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
- Narrative Check: [PASS/CAUTION/NARRATIVE-DRIVEN]

**Jevons Paradox:** [FAVORABLE/UNFAVORABLE/NEUTRAL]
- [reasoning]

**Build-vs-Buy Vulnerability:** [HIGH/MEDIUM/LOW]
- [reasoning]

**Survival Fitness:** [STRONG/ADEQUATE/CONCERNING/CRITICAL]
- FCF: [assessment]
- SBC: [assessment]
- Debt: [assessment]

**Lens Interactions:** [identify any patterns from section 3]

**Overall Assessment:** [summary]
```

## Integration Notes

- This skill complements general web search for news
- Always cite data sources (Finnhub, news articles)
- For complex analysis, apply lenses sequentially
- Track classification changes over time in memory
- The interplay between lenses is where the insight lives

## Files

- `scripts/fh` — Finnhub CLI wrapper
- `scripts/finnhub-cli.py` — Python API client
- `docs/` — Detailed lens documentation
- `examples/` — Sample analyses
