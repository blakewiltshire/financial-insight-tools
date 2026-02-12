# Financial Insight Tools (FIT) — Quick Start

This guide covers first-run setup and initial orientation.

---

## 1) Clone the Repository

```bash
git clone https://github.com/blakewiltshire/financial-insight-tools.git
cd financial-insight-tools
```

---

## 2) Create a Virtual Environment

```bash
python3 -m venv .venv
```

If `python3` is not available on your system, try:

```bash
python -m venv .venv
```

---

## 3) Activate the Environment

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

---

## 4) Install Requirements

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5) Launch the Application

```bash
streamlit run app.py
```

The application will launch at:

http://localhost:8501

---

## 6) First Orientation

Start with **Market & Volatility Scanner** to establish distribution and regime context.

Then explore:

- **Trade Structuring & Risk Planning** for scenario modelling  
- **Economic Exploration** for macro landscape analysis  
- **Cross-Asset Correlation** for relationship mapping  
- **Observation & Export** for structured artefact assembly  

Configuration and registry files are read at process start. Restart the Streamlit process after modifying configuration files.

---

## 7) Outputs

Most modules support structured CSV/JSON exports suitable for documentation, downstream analysis, or AI-assisted interpretation workflows.

> Note: FIT writes local artefacts (exports, bundles, snapshots) into the project directory. These are intended for local use and are not persisted across deployments.

---

Financial Insight Tools by Blake Wiltshire  
© Blake Media Ltd.
