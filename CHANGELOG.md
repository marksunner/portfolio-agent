# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-03-02

### Added
- **Lens Interaction Patterns** — Five named patterns for deeper analytical insight:
  - "Right Thesis, Wrong Vehicle" (Jevons favorable + Survival concerning)
  - "Tactical Opportunity in Structural Uncertainty"
  - "Moat Under Siege"
  - "Fortress Position"
  - "Narrative vs Reality"

- **Classification History Tracking** (`classify.py`)
  - `list` — Current When→If classifications
  - `history <SYMBOL>` — Classification history with catalysts
  - `update <SYMBOL> <CLASS> <CATALYST>` — Record classification changes
  - `alerts` — Recent transitions (last 30 days)

- **Portfolio-Level Analysis** (`portfolio.py`)
  - `concentration` — Sector concentration risk analysis
  - `correlation` — Correlated catalyst exposure mapping
  - `summary` — Full portfolio health summary

- **Contrarian Scoring** (`contrarian.py`)
  - Formula: Tactical Severity × Structural Soundness × Jevons Favorability
  - Identifies tactical overselling opportunities
  - Score 60+ = strong, 30-60 = moderate, <30 = weak

- **Earnings Calendar** (`earnings.py`)
  - `upcoming [DAYS]` — Portfolio earnings in next N days
  - `check <SYMBOL>` — Specific symbol lookup
  - `alert` — 7-day horizon for morning checks
  - `week` — This week's calendar
  - Flags TRANSITION positions needing pre-earnings review

- **Financial Endpoints** (finnhub-cli.py)
  - `financials <SYMBOL>` — P/E, FCF, margins, debt ratios
  - `earnings <SYMBOL>` — Earnings history with surprises
  - `recommendations <SYMBOL>` — Analyst sentiment and trends
  - `peers <SYMBOL>` — Peer companies for relative valuation

- **Narrative Detection** — Added to Tactical vs Structural guidance
  - Source credibility checks
  - Author incentive analysis
  - Analytical substance verification
  - Propagation pattern assessment

- **Rate Limit Guidance** — API budget priorities for free tier (60 calls/min)

### Fixed
- **Critical:** Shell wrapper path bug — scripts now resolve paths relative to themselves

### Changed
- SKILL.md restructured with new capability sections
- README updated with comprehensive usage documentation

## [1.0.0] - 2026-03-01

### Added
- Initial release
- Six-lens analysis framework
- Basic Finnhub integration (quote, quotes, news, profile)
- SKILL.md for OpenClaw agent integration
- Example analyses for VRT and ANET
