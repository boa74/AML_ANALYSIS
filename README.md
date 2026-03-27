# Anti-Money Laundering (AML) Transaction Analysis

Exploratory Data Analysis for detecting suspicious financial transaction patterns using statistical methods and network analysis.

## 📋 Project Overview

This project demonstrates analytical techniques for identifying potential money laundering patterns in international wire transfer transactions. The analysis follows **FATF** (Financial Action Task Force) and **ACAMS** guidelines.

**Analysis Scope**: 862,296 suspicious transactions  
**Key Focus**: Cross-border flows, intermediary detection, threshold analysis

> **Note**: Due to confidentiality agreements, the original dataset cannot be shared. This repository includes a **synthetic data generator** that creates demonstration data with similar structure and patterns.

## 🎯 Analysis Components

### 1. Univariate Profiling
- Transaction amount distribution analysis
- Country frequency analysis (sender/beneficiary)
- Customer segment distributions
- Missing data pattern identification

### 2. Bivariate Analysis
- **Sender ↔ Beneficiary country flows** (cross-tabulation)
- Row-normalized concentration analysis
- High-risk corridor identification
- Segment-specific flow patterns

### 3. Network Analysis
- Transaction network graph construction (NetworkX)
- **Hub country identification** using degree centrality
- Intermediary route analysis (up to 4 hops)
- **Round-tripping detection** (same origin-destination via intermediaries)

### 4. Feature Engineering
- Absolute threshold flags (e.g., $10,000 reporting threshold)
- Z-score normalization (sender/beneficiary relative)
- Offshore hub indicators (9 jurisdictions)
- Intermediary depth counters (0-4 levels)

## 🔍 Key Findings (Original Dataset)

- **Hub Countries**: France and US identified as major beneficiary hubs
- **High-Risk Corridors**: Ireland→US (60%+ concentration), UAE→France, HongKong→India
- **Intermediary Impact**: Transactions with intermediaries show **2-3x higher median amounts**
- **Round-Tripping**: 5-8% of transactions return to origin country via intermediaries
- **Threshold Clustering**: Significant concentration near $10K regulatory threshold

## 📊 Visualizations Included

- **18 Heatmaps**: Sender-Beneficiary country flows, row-normalized patterns
- **Network Graphs**: Country hubs with degree centrality
- **Threshold Analysis**: Transaction concentration near regulatory limits
- **Distribution Plots**: Amount analysis, log-scale transformations
- **Bar Charts**: Top countries, segments, routes

Total: **56 visualizations**

## 🛠️ Technical Stack

```
Python 3.8+
├── pandas              # Data manipulation
├── numpy               # Numerical analysis
├── matplotlib          # Plotting
├── seaborn            # Statistical visualization
├── networkx           # Graph/network analysis
└── pycountry          # Country code standardization
```

## 📁 Project Structure

```
AML_ANALYSIS/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── AML_EDA_Portfolio.ipynb            # Main analysis notebook (with synthetic data)
└── data_generator.py                  # Synthetic transaction data generator
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Run Analysis

```bash
# Open Jupyter notebook
jupyter notebook AML_EDA_Portfolio.ipynb
```

The notebook is self-contained with:
- **Synthetic data generation** (runs automatically)
- **Complete EDA workflow** (5 sections)
- **All visualizations** (generated from synthetic data)

### 3. Generate Your Own Data

```python
from data_generator import generate_aml_transactions

# Generate synthetic dataset
df = generate_aml_transactions(
    n_transactions=50000,
    n_countries=50,
    intermediary_rate=0.25
)
```

## 🎓 Skills Demonstrated

### Technical Skills
- **Statistical Analysis**: Z-scores, HHI, Entropy, percentile analysis
- **Graph Theory**: NetworkX centrality metrics, path analysis
- **Data Visualization**: Heatmaps, network graphs, distributions
- **Feature Engineering**: 12+ derived risk indicators
- **Python**: Pandas, NumPy, advanced data manipulation

### Domain Knowledge
- AML/CFT compliance standards (FATF, ACAMS)
- Financial crime typologies (layering, structuring, round-tripping)
- Regulatory thresholds (Bank Secrecy Act)
- Cross-border transaction analysis

### Analytical Approach
- Univariate → Bivariate → Multivariate progression
- Pattern recognition in high-dimensional data
- Network-based anomaly detection
- Business-driven feature engineering

## 📈 Methodology Highlights

### 1. Concentration Metrics
```python
# Herfindahl-Hirschman Index (HHI)
HHI = sum(share^2 for each destination)

# Shannon Entropy
Entropy = -sum(p * log(p) for each destination)
```

### 2. Network Centrality
```python
# Degree centrality (hub identification)
degree_centrality = number_of_connections / (n_nodes - 1)
```

### 3. Z-Score Normalization
```python
# Sender-relative amount
z_score = (amount - sender_mean) / sender_std
```

## 📚 AML Concepts Applied

- **Layering**: Multi-hop transactions obscuring origin/destination
- **Structuring**: Breaking amounts to avoid reporting thresholds
- **Round-Tripping**: Funds leaving and returning to origin country
- **Hub Detection**: Countries with disproportionate inbound/outbound flows
- **Corridor Analysis**: Bilateral flow concentration patterns

## ⚖️ Privacy & Compliance

This repository:
- ✅ **No raw transaction data** (NDA protected)
- ✅ **Synthetic data only** (demonstrational purposes)
- ✅ **No PII** (no customer identifiers)
- ✅ **Methodology focus** (generalizable approach)

**Safe for GitHub/Portfolio sharing** ✓

## 📧 Contact

**Analyst**: Boa Kim  
**LinkedIn**: https://www.linkedin.com/in/boah-kim/  
**Project Date**: March 2026

---

## 🌟 Why This Project Stands Out

1. **Real-world scale**: Methodology tested on 860K+ transactions
2. **Industry standards**: Follows FATF/ACAMS compliance guidelines
3. **Network analysis**: Graph theory application (not just SQL/pandas)
4. **Feature engineering**: Domain-driven risk indicators
5. **Reproducible**: Synthetic data generator included

---

*This project demonstrates EDA and analytical capabilities for financial crime detection. The methodology is production-ready and has been validated on confidential real-world data (not included).*
