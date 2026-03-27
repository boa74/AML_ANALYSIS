# Detecting Hidden Behavioral Patterns in Anti-Money Laundering (AML) Transactions

## 📌 Project Overview
This project develops a machine learning–driven AML detection framework to identify hidden behavioral and structural patterns in transaction data beyond traditional rule-based systems.

While rule-based AML systems rely on predefined thresholds, they often fail to capture complex behaviors such as layering, structuring, and multi-intermediary routing. This project addresses those limitations by combining feature engineering, network analysis, and unsupervised anomaly detection approaches.

---

## 🎯 Objective
- Identify anomalous transaction patterns not captured by rule-based systems  
- Design a structured analytical workflow for AML detection  
- Explore hidden behavioral patterns in transaction data  
- Improve interpretability and prioritization of high-risk transactions  

---

## 📊 Data
- ~860K international transaction records  
- Cross-border transaction flows  
- Sender / beneficiary information  
- Intermediary routing structures  

*Note: Synthetic data is used in this repository to ensure confidentiality while preserving real-world data characteristics.*

---

## 📁 Repository Scope
This repository focuses on the **exploratory analysis, feature engineering, and network-based investigation components** of the project.

Included:
- Exploratory Data Analysis (EDA)
- Feature engineering aligned with AML typologies
- Network-based transaction analysis
- Behavioral pattern exploration using synthetic data

These components demonstrate the analytical foundation of the full research in a reproducible and privacy-safe format.

---

## 🔬 Extended Research Scope
In the full research study, this work was extended with **unsupervised anomaly detection and ensemble modeling**:

- Applied multiple anomaly detection models:
  - HBOS (distribution-based detection)
  - PCA (multivariate structural anomalies)
  - Isolation Forest (sparse region detection)
  - ECOD (distribution irregularities and missingness)

- Compared model behavior and detection patterns  
- Designed percentile-based risk stratification (Top 5–10%)  
- Developed ensemble approaches combining models for improved robustness  

These methods revealed **latent behavioral patterns** not captured by traditional AML systems.

---

## ⚙️ Methodology

### 1. Feature Engineering
- Transaction threshold indicators  
- Z-score normalization  
- Intermediary depth (multi-hop routing)  
- High-risk country flags  
- Burst behavior features (short-term frequency patterns)  

---

### 2. Behavioral Analysis
- Univariate and multivariate analysis  
- Correlation and distribution exploration  
- Network analysis of transaction flows  

---

### 3. Modeling Approach (Research Extension)
- Unsupervised anomaly detection  
- Model comparison across behavioral dimensions  
- Ensemble modeling for improved detection stability  

---

## 🔍 Key Findings
- Hidden behavioral layers exist beyond rule-based AML detection  
- Different models capture distinct anomaly types:
  - Burst behavior  
  - Structural complexity  
  - Large-scale anomalies  
  - Missing or opaque information  
- Ensemble approaches improve detection robustness and consistency  
- High-risk transactions concentrate within top percentile ranges  

---

## 💼 Business Impact
- Improves detection of complex AML patterns (layering, structuring)  
- Reduces false positives and manual investigation workload  
- Enables prioritization of high-risk transactions  
- Supports scalable and interpretable AML monitoring systems  

---

## 🛠️ Tech Stack
- Python (Pandas, NumPy)  
- NetworkX (graph analysis)  
- Matplotlib / Seaborn  
- SQL  

---

## 🧠 Key Skills Demonstrated
- Feature engineering for financial risk detection  
- Unsupervised anomaly detection design and interpretation  
- Model comparison and behavioral analysis  
- Network-based transaction modeling  
- Translating analytical results into business insights  

---

## 🚀 Future Work

The full research includes unsupervised anomaly detection modeling, model comparison, and ensemble design. 
The corresponding implementation and visualizations will be added to this repository in a future update. 

---

## 📌 Why This Project Matters
This project goes beyond exploratory analysis by demonstrating how machine learning can enhance AML systems through detection of hidden behavioral patterns. It reflects a real-world transition from rule-based systems to data-driven risk detection frameworks.

---

## 📫 Contact
Boa Kim  
Columbia University – Applied Analytics  
LinkedIn: https://www.linkedin.com/in/boah-kim/