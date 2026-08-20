# HealthSentinel: Healthcare Operations Intelligence Dashboard

**HealthSentinel** is an enterprise-grade Public Health Analytics & Healthcare Operations Intelligence Dashboard built with Streamlit, Python, and Plotly. It provides decision-makers, public health officials, and researchers with actionable analytics derived from a robust star-schema data warehouse model.

---

## 🚀 Dashboard Suite Overview

The application features a 7-page multi-page navigation structure wired via `st.navigation` in `app.py`:

| # | Page Name | Status | Key Features & Analytics |
|---|---|---|---|
| **0** | **Home** | ✅ Built | Hero introduction, executive summary highlights, quick navigation links, and system overview. |
| **1** | **Executive Public Health Overview** | ✅ Built | Dual-tab dashboard (Executive Summary + Disease Surveillance), universal sidebar filters, KPI cards, case fatality rate (CFR) trends, state rankings, and risk scoring. |
| **2** | **Geographic & Environmental Intelligence** | ✅ Built | Spatial heatmaps, Air Quality Index (AQI) tracking, rainfall analytics, sanitation scores, and environmental risk correlation with disease outbreaks. |
| **3** | **Laboratory & Healthcare Capacity** | ✅ Built | Testing volumes, positivity rates, ICU and hospital bed occupancy metrics, lab efficiency, and vaccination coverage. |
| **4** | **Outbreak Monitoring & Forecasting** | ✅ Built | Early warning outbreak detection, alert triggers, containment tracking, trend forecasting, and Decision Snapshots. |
| **5** | **Health Programs & Population Vulnerability** | ✅ Built | Public health program reach, beneficiary coverage, vulnerability indexing, and urban vs. rural healthcare disparity analysis. |
| **6** | **Upload & Custom Analysis** | ✅ Built | Ad-hoc CSV dataset upload, custom query engine, data quality inspection, and PDF/Excel report export. |

---

## 📁 Project Structure

```text
HealthSentinel/
├── app.py                                                # Application entry point & multi-page navigation setup
├── requirements.txt                                      # Python package dependencies
├── .gitignore                                            # Git exclusion rules for bytecode, caches, & environments
├── README.md                                             # Project documentation
├── .streamlit/
│   └── config.toml                                      # Corporate visual theme configuration
├── assets/                                               # Application branding logos & visual assets
│   ├── home_hero.png
│   ├── logo_full.png
│   └── logo_icon.png
├── dashboards/                                           # Multipage Streamlit dashboard views
│   ├── 00_Home.py                                        # Landing page & suite introduction
│   ├── 0_Executive_Public_Health_Overview.py             # Executive metrics & disease surveillance
│   ├── 1_Geographic_Environmental_Intelligence.py        # Environmental & geographic risk analysis
│   ├── 2_Laboratory_Healthcare_Capacity.py               # Lab testing & healthcare capacity metrics
│   ├── 3_Outbreak_Monitoring_Forecasting.py              # Outbreak monitoring & predictive snapshots
│   ├── 4_Health_Programs_Population_Vulnerability.py    # Health program coverage & population risk
│   └── 5_Upload_Custom_Analysis.py                      # Custom file upload & interactive ad-hoc query
├── src/                                                  # Core data processing & UI rendering modules
│   ├── data_loader.py                                    # Primary cached CSV data loader & star-schema join engine
│   ├── filters.py                                        # Universal sidebar filter panel component
│   ├── geographic.py                                     # Map generation & spatial chart rendering helpers
│   ├── kpis.py                                           # KPI calculation engine & statistical formulas
│   ├── pdf_report.py                                     # Automated PDF report generation (ReportLab)
│   ├── programs_data_loader.py                           # Dedicated data loader for health program metrics
│   ├── programs_filters.py                              # Specialized filter controls for program views
│   ├── programs_kpis.py                                 # Health program specific KPI logic
│   ├── programs_styling.py                              # Visual styling utilities for health program views
│   ├── report_generator.py                              # Comprehensive PDF & summary report compiler
│   └── styling.py                                        # Global CSS stylesheet & custom HTML card components
├── Cleaned datasets/                                     # Processed star-schema CSV tables
│   ├── dim_dates_cleaned.csv                             # Date dimension table
│   ├── dim_disease_cleaned.csv                           # Disease dimension table
│   ├── dim_program_cleaned.csv                           # Public health program dimension table
│   ├── dim_source_cleaned.csv                            # Data source dimension table
│   ├── dim_state_cleaned.csv                            # Geographic state/region dimension table
│   ├── fact outbreak cleaned.csv                         # Outbreak monitoring fact table
│   ├── fact_disease_surveillance_cleaned.csv            # Disease surveillance fact table
│   ├── fact_environmental_cleaned.csv                   # Environmental indicators fact table
│   └── fact_lab_healthcare_cleaned.csv                  # Laboratory & healthcare capacity fact table
├── Raw data/                                             # Original uncleaned raw data extracts
├── Data Cleaning codes/                                  # Data preprocessing ETL scripts & notebooks
└── EDA/                                                  # Exploratory Data Analysis notebooks & statistical scripts
```

---

## 📊 Data Model Architecture

The core data model follows a **Star Schema** architecture, linking dimension lookup tables with granular fact tables:

### Dimension Tables
| Table | Grain | Key Columns |
|---|---|---|
| `dim_dates` | 1 row per month | `date_id`, `year`, `month_name`, `quarter` |
| `dim_state` | 1 row per state | `state_id`, `state_name`, `region`, `population` |
| `dim_disease` | 1 row per disease | `disease_id`, `disease_name`, `disease_category` |
| `dim_source` | 1 row per reporting source | `source_id`, `source_name` |
| `dim_program` | 1 row per health program | `program_id`, `program_name` |

### Fact Tables
| Table | Grain | Key Metrics & Measures |
|---|---|---|
| `fact_disease_surveillance` | State × Date × Disease × Source | Reported cases, active cases, recovered cases, deaths, CFR, recovery rate, risk score |
| `fact_outbreak` | State × Date × Disease × Source | Outbreak alerts, warning level, containment rate, impacted population |
| `fact_environmental` | State × Date | Air Quality Index (AQI), rainfall (mm), sanitation coverage, environmental risk index |
| `fact_health_programs` | State × Date × Program | Program coverage %, beneficiaries reached, population vulnerability index |
| `fact_lab_healthcare` | State × Date | Diagnostic tests conducted, positivity rate %, ICU bed occupancy, hospital beds, vaccination coverage |

---st.markdown("""
## 📐 Key KPI Definitions & Calculation Logic

| KPI | Formula / Calculation Method |
|---|---|
| **Total Population Under Surveillance** | $\sum \text{population\\_under\\_surveillance}$ for unique filtered regions |
| **Total Reported Cases** | $\sum \text{total\\_reported\\_cases}$ |
| **Case Fatality Rate (CFR %)** | $\frac{\sum \text{deaths}}{\sum \text{total\\_reported\\_cases}} \times 100$ *(Aggregated ratio)* |
| **Recovery Rate (%)** | $\frac{\sum \text{recovered\\_cases}}{\sum \text{total\\_reported\\_cases}} \times 100$ *(Aggregated ratio)* |
| **Positivity Rate (%)** | $\frac{\sum \text{positive\\_tests}}{\sum \text{total\\_tests}} \times 100$ |
| **Public Health Risk Score** | Mean of `public_health_risk_score` across filtered records |

> **Note on Aggregation:** Percentage metrics (CFR, Recovery Rate, and Positivity Rate) are recomputed from aggregated sums rather than averaged row-level percentages to prevent skewing and volume bias across states/diseases.
""")
---

## 🛠️ Installation & Running Locally

### Prerequisites
* Python 3.10+ installed on your system.

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NanubalaSravani/Development-of-a-Healthcare-Operations-Intelligence-Dashboard-with-Decision-Analytics-Group-2.git
   cd Development-of-a-Healthcare-Operations-Intelligence-Dashboard-with-Decision-Analytics-Group-2
   ```

2. **Set Up Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

5. **Access Dashboard:**
   Open your browser and navigate to `http://localhost:8501`.

---

## 💡 Key Architectural Highlights

* **Single Entry Point Multipage Navigation:** Built using Streamlit's `st.navigation` and `st.Page` API for seamless sidebar switching without reloading state.
* **Unified High-Contrast Plotly Theme:** Configured custom Plotly templates in `app.py` forcing all chart text, axes, tick marks, and legends to crisp black `#000000` text for maximum legibility.
* **Modular Codebase:** Business logic, KPI calculations, styling, and data loading are cleanly separated into the `src/` directory.
* **Automated PDF Reporting:** Built-in PDF generation engine using `reportlab` allows users to export executive summaries and dashboard snapshots directly.
