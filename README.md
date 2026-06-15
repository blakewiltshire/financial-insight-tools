# Financial Insight Tools (FIT) — Structured Financial Reasoning Environment

Financial Insight Tools (FIT) is a modular research environment for exploring financial markets, macroeconomic structure, portfolio construction, cross-asset relationships, transmission dynamics, positioning structure, company analysis, and structured reasoning workflows through a consistent analytical framework.

FIT provides consistent structure across distribution analysis, trade modelling, macroeconomic exploration, thematic correlation, relative macro transmission, positioning analysis, company structure review, and observation capture so that information can be organised, examined, aligned, and carried forward into documentation, research workflows, or AI-assisted reasoning environments.

---

## Companion References (PDF)

FIT includes companion documents under `docs/`:

- *Crafting Financial Frameworks — Modular, AI-Ready Systems for Structured Decision Support*
- *Financial Insight Tools — Unified Index & Glossary Reference*

These documents provide architectural framing and consolidated reference material.

Note: GitHub’s in-browser PDF preview may not render complex code-block formatting reliably; download for the best viewing experience.

---

## Python Version

Python (tested on 3.12.x)

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/blakewiltshire/financial-insight-tools.git
cd financial-insight-tools
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

If `python3` is not available on your system, try:

```bash
python -m venv .venv
```

### 3. Activate the Environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (cmd)**

```bat
.\.venv\Scripts\activate.bat
```

### 4. Install Requirements

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will launch at:

http://localhost:8501

---

## What This Is (and Isn’t)

**Is:**  
A structured, modular environment for examining financial data, macroeconomic indicators, portfolio behaviour, trade scenarios, cross-market relationships, and system-level interaction through consistent analytical scaffolds.

**Isn’t:**  
A brokerage platform, automated trading system, signal engine, portfolio manager, advisory service, or predictive model. FIT does not execute trades, provide financial advice, or generate investment recommendations.

All outputs are structural and exploratory in nature.

---

## Platform Architecture

FIT is structured across three connected analytical layers.

### System Foundation

- Economic Exploration
- Thematic Correlation
- Relative Macro Transmission
- Positioning & Crowding

These modules frame macro conditions, systemic relationships, transmission pathways, and market participation structure.

---

### Financial Application

- Market & Volatility Scanner
- Company Structure Review
- Asset Snapshot Generator
- Trade Timing & Confirmation
- Price Action & Trend Confirmation
- Trade Structuring & Risk Planning
- Spread Ratio Insights
- Cross Asset Correlation
- Live Portfolio Monitor

These modules apply structural context to scenario analysis, portfolio framing, and market inspection.

---

### Utility & Decision Support

- Kelly Criterion
- VaR Calculator
- Compounding Calculator
- Standard Deviation Calculator
- Historical Data Currency Converter
- Data Cleaner & Inspector
- Observation & Export Bundle Builder

These modules support operational consistency, validation, and structured documentation workflows.

---

## Screenshots

---

### Unified Launcher — Structural Orientation

![Unified Launcher](docs/screenshots/01-launcher.png)

The unified launcher presents FIT’s modular architecture and clarifies:

- the analytical domains available
- how modules interrelate
- where configuration, observation, and export functions reside

This is the orientation layer before moving into structured analysis.

---

### Economic Exploration — Macro System View

![Economic Exploration](docs/screenshots/02-economic-exploration.png)

A structural view across macroeconomic conditions and country-level indicators:

- growth, inflation, labour, and trade signals
- thematic grouping and indicator structure
- cross-country comparison and aggregation
- system-level economic context

Provides the macro foundation for downstream analytical workflows.

---

### Thematic Correlation — Relationship Mapping

![Thematic Correlation](docs/screenshots/03-thematic-correlation.png)

A structural view across macroeconomic themes and systemic relationships:

- thematic clustering across economic indicators
- direct and inverse relationships
- macro alignment and divergence
- cross-country and cross-theme co-movement

This provides the relationship layer before transmission analysis.

---

### Relative Macro Transmission — Exogenous Differential Architecture

![Relative Macro Transmission](docs/screenshots/04-relative-macro-transmission.png)

Tracks exogenous differentials across systems and how macro pressure transmits through markets:

- growth and inflation differentials
- interest rate and carry structures
- external balance and FX pressure
- sovereign, equity, and cross-market divergence

This moves beyond correlation into structural transmission analysis.

---

### Positioning & Crowding — Position Architecture

![Positioning & Crowding](docs/screenshots/05-positioning-crowding.png)

A structural view across leveraged positioning, percentile extremes, and market participation behaviour:

- Commitment of Traders (COT) positioning
- percentile extremes and crowding conditions
- positioning turns and reversal structures
- market overlay and regime interpretation

This provides the participant behaviour layer across major futures markets.

---

### Market & Volatility Scanner — Distribution Backbone

![Market Scanner](docs/screenshots/06-market-scanner.png)

A structural view across market behaviour and volatility conditions:

- frequency and dispersion metrics
- shape characteristics
- regime-sensitive return framing
- structural probability context

Provides quantitative grounding for downstream modelling.

---

### Trade Structuring & Risk Planning — Scenario Architecture

![Trade Structuring](docs/screenshots/07-trade-structuring.png)

A structured view across trade construction and risk framing:

- entry and stop structure
- exposure calibration
- position sensitivity
- scenario-based evaluation

Supports analytical evaluation without automating execution.

---

### Build Export Bundle — Structured Artefact Assembly

![Export Bundle](docs/screenshots/08-export-bundle.png)

The export module organises analytical components into structured bundles for documentation, research artefacts, and AI-assisted workflows.

Outputs preserve linkage to the underlying analytical structure.

---

## Where to Start

- **Economic Exploration** — macro system structure and country-level diagnostics
- **Thematic Correlation** — relationship mapping across macroeconomic themes
- **Relative Macro Transmission** — exogenous differential analysis and regime divergence
- **Positioning & Crowding** — leveraged positioning, percentile extremes, and positioning turns
- **Market & Volatility Scanner** — distribution structure and regime context
- **Trade Structuring & Risk Planning** — scenario modelling and exposure framing
- **Observation & Export** — structured artefact assembly for documentation and AI workflows

Each module presents a different perspective on the same underlying analytical framework without fragmenting or redefining it.

---

## Structure (High-Level)

```text
financial-insight-tools/
  apps/          # Modular application domains
  core/          # Shared structural logic and helpers
  constants/     # Configuration and registry mappings
  docs/          # Reference documentation
  templates/     # Custom templates
  brand/         # Visual assets
  data/          # Optional local datasets
  images/        # Application images
  app.py         # Streamlit launcher
  LICENSE
  requirements.txt
  README.md
```

Canonical resources live alongside the modules that use them.  
Generated artefacts are produced locally during use.

---

## Updating & Extending FIT

### Updating the Framework

Updates to Financial Insight Tools are distributed through the Git repository.

From the project root:

```bash
git pull
```

Only files that have changed in the repository will be updated locally.

Regular updates include:

- Historical asset price datasets refreshed on a regular weekly maintenance cadence
- Weekly positioning and Commitment of Traders (COT) dataset updates
- Macroeconomic datasets updated as new releases become available
- Refinements to shared universal configuration layers
- Module-level enhancements where applicable

If you have modified local files, commit or back them up before pulling updates to avoid merge conflicts.

After pulling updated historical asset data, rerun the **Asset Snapshot Scanner** to regenerate summary outputs where applicable.

---

### Universal and Country Layers

FIT uses a layered configuration model.

**Universal files** define shared behaviour across the system:

- `universal_indicator_map`
- `universal_insights`
- `universal_routing`
- `universal_scoring_weights_labels`
- `universal_use_cases`
- `universal_visual_config`

These files establish common structural logic and may be updated as the framework evolves.

**Country-level files** define jurisdiction-specific implementations:

- `indicator_map`
- `insights`
- `routing`
- `scoring_weights_labels`
- `use_cases`
- `visual_config`

If extending the system with additional indicators or jurisdictions, implement changes at the country level first.

If a new indicator requires shared scoring, routing, or visual logic across the system, corresponding updates may also be required in the universal layer.

---

### Data Update Policy

- Historical financial asset datasets are refreshed on a regular cadence.
- Weekly positioning datasets are updated through Commitment of Traders (COT) releases.
- Macroeconomic datasets are updated as new releases become available.
- Updates modify canonical data files under `apps/data_sources/...`.

Local artefacts (exports, snapshots, observations) are not modified by repository updates.

---

FIT is designed as an open, extensible system. Users may extend or adapt the framework as required. Structural coherence is maintained by preserving the distinction between universal layers and local implementations.

---

## License & Use

Free to read and use as provided.

All outputs are structural and exploratory in nature.  
No advisory, brokerage, portfolio management, or automated trading services are provided.

Refer to LICENSE for details.

---

## Ecosystem Context

Financial Insight Tools forms part of a broader independent framework studio exploring complex systems through structured guides, modular tools, and applied insight.

FIT aligns with the architectural concepts presented in the *Navigating the World of Economics, Finance, and Markets* series — a structured examination of economics and finance as interconnected systems shaped by institutions, incentives, coordination mechanisms, and technological change.

The series spans six thematic areas: Foundational Knowledge, Practical Economics, Finance Fundamentals, Investment Strategies, Trading and Operations, and FinTech Innovations. Together, these areas provide a coherent framework for understanding macroeconomic structure, market dynamics, portfolio construction, and system-level behaviour.

Each guide functions as a self-contained analytical unit while aligning to a broader modular architecture that supports structured reasoning, comparative analysis, and cross-domain exploration.

Financial Insight Tools operationalises elements of this framework in an applied research environment. The application can be used independently; the guides provide deeper architectural framing for those exploring the underlying structural model.

Further context:  
https://blakewiltshire.com

---

Financial Insight Tools by Blake Wiltshire  
© Blake Media Ltd.
