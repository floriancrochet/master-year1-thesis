# S&P 500 Index Tracking using Penalized Regression
This project replicates the S&P 500 index using sparse penalized regression techniques.

[**Thesis (PDF – online)**](https://drive.google.com/file/d/11zS62i8TvMN_il1KhHIQ_zXpZ7_0lr5X/view?usp=drive_link) • [**Executive Summary (PDF – online)**](https://drive.google.com/file/d/1r2AJqVG56BK5bwb2dM1LxY2Q1q9jXPcR/view?usp=drive_link) • [**Data Visualization App**](https://master-year1-thesis.onrender.com)

---

## 🎯 Overview

**Objectives**
- Construct sparse portfolios that replicate S&P 500 returns
- Identify stable subsets of assets using penalized regression
- Evaluate replication performance via tracking and risk metrics
- Provide a reproducible analytical framework for ETF design

---

## 🗄️ Data
- **Source:** Yahoo Finance and `data/base_index_tracking.xlsx`
- **Time Period / Size:** 2017-01-01 to 2024-03-15
- **Target Variable:** S&P 500 daily returns
- **Key Predictors / Features:** Individual S&P 500 constituent stock returns
- **Preprocessing:** Handled missing values, filtered market holidays, and adjusted outliers using Boudt robust method
- **Data Availability:** Publicly available via `tidyquant` API, processed mock data are provided in `data/`

---

## 🧠 Methodology
- **Theoretical Approach:** Sparse index replication
- **Mathematical Framework:** Penalized regression (Ridge, Lasso, Elastic Net, Adaptive Lasso) with non-negativity constraints and Distance Correlation Sure Independence Screening (DC-SIS)
- **Evaluation Strategy:** Time series rolling-origin cross-validation (504-day window, 21-day horizon)

---

## ⚙️ Features
- **Apply Penalized Regression:** Accommodate non-negativity constraints for portfolio weights
- **Implement Variable Screening:** Reduce dimensionality via Distance Correlation Sure Independence Screening
- **Prevent Look-Ahead Bias:** Execute robust testing via rolling-origin cross-validation
- **Compare Models:** Evaluate Ridge, Lasso, Elastic Net, and Adaptive Lasso performance
- **Calculate Portfolio Metrics:** Extract Tracking Error, Beta, Information Ratio, and Jensen's Alpha
- **Visualize Interactive Results:** Manage application state through a dedicated dashboard

---

## 🧰 Tech Stack
- **Language:** R / Python >=3.11
- **Data Engineering & Acquisition:** tidyquant, readxl, pandas-datareader
- **Numerical Computing & Data Manipulation:** tidyverse, xts, zoo, pandas, numpy, geopandas, openpyxl
- **Econometrics & Statistical Inference:** statsmodels
- **Time Series Analysis:** urca, fBasics, forecast
- **Machine Learning & Deep Learning:** glmnet, caret, VariableScreening
- **Quantitative Finance:** PerformanceAnalytics
- **Data Visualization:** corrplot, patchwork, plotly
- **Dashboards & Web APIs:** dash, dash-auth, dash-bootstrap-components, dash-bootstrap-templates, gunicorn

---

## 📦 Installation

```bash
git clone https://github.com/floriancrochet/master-year1-thesis.git
cd master-year1-thesis
uv sync
```

---

## 💻 Usage Example

### Reproducing the Analysis / Execution Pipeline

```bash
uv run python dashboard/thesis_data_visualization.py
```

```r
library(glmnet)

# Example: Fit a penalized regression model with DC-SIS
model <- dcsis_glmnet_function("adlasso_dcsis", grid)
coefficients <- model$model_coefs
```

---

## 📂 Project Structure

```text
master-year1-thesis/
│
├── dashboard/
│   └── thesis_data_visualization.py
├── data/
│   ├── base_index_tracking.xlsx         # S&P 500 constituent returns
│   ├── coefficients.csv
│   ├── data_performance.csv
│   ├── hyperparameters.csv
│   ├── nb_variables.csv
│   └── performance.csv                  # Out-of-sample metrics
├── report/
│   ├── executive_summary.pdf
│   └── thesis.pdf
├── src/
│   └── thesis.qmd                       # Penalized regression & DC-SIS
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
├── master-year1-thesis.Rproj
├── pyproject.toml
└── uv.lock
```

---

## 📈 Results

### Performance Metrics
| Model / Strategy               | Assets | Tracking Error | Beta   | Info Ratio | Active Return | Jensen's Alpha |
|--------------------------------|--------|----------------|--------|------------|---------------|----------------|
| Baseline (S&P 500)             | 484    | 0.0000         | 1.00   | NA         | 0.0000        | 0.0000         |
| **Adaptive Lasso**             | **143** | 0.0201         | 1.03   | **1.82**   | **0.0365**    | **0.0322**     |
| Lasso                          | 198    | **0.0198**     | 1.03   | 1.77       | 0.0350        | 0.0309         |
| *Adaptive Lasso (DC-SIS)*      | *138*  | *0.0316*       | *0.99* | *0.13*     | *0.0040*      | *0.0048*       |

### Key Findings
- **Lasso Model:** Achieved the lowest tracking error by isolating the 198 most informative constituent assets
- **Adaptive Lasso Model:** Delivered superior risk-adjusted returns (143 assets), penalizing weak predictors while retaining key large-cap constituents
- **Distance Correlation SIS:** Improved variable stability but introduced a modest increase in tracking error via aggressive dimensionality reduction

---

## 📚 References
- Székely et al. (2007) – *Measuring Dependence by Correlation of Distances*
- Tibshirani (1996) – *Regression Shrinkage and Selection via the Lasso*
- Wu & Yang (2014) – *Nonnegative Elastic Net for Index Tracking*
- Zou (2006) – *The Adaptive Lasso and Its Oracle Properties*

---

## 📜 License
This project is released under the MIT License.  
© 2025 Florian Crochet

---

## 👤 Author
**Florian Crochet**  
[GitHub Profile](https://github.com/floriancrochet)

*Master 1 – Econometrics & Statistics, Applied Econometrics Track*

---

## 🤝 Acknowledgments
This work was supervised by Mr. Olivier Darné.
