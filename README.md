# Index Tracking and Asset Selection Using Penalized Regression  
*A research-driven framework for constructing sparse S&P 500 tracking portfolios using penalized regression and robust econometric validation.*

---

## 📘 Overview  
This project implements an econometric framework to replicate the S&P 500 index with a reduced subset of its constituent stocks using sparse penalized regression techniques under non-negativity constraints. The objective is to balance replication accuracy with portfolio simplicity and cost-efficiency, reflecting realistic ETF construction conditions.

The work applies Ridge, Lasso, Elastic Net, and Adaptive Lasso regressions combined with Distance Correlation Sure Independence Screening (DC-SIS) and rolling-origin cross-validation to ensure robust, interpretable, and stable replication portfolios over the period 2017–2024.

**Objectives**  
- Construct sparse portfolios that closely track the S&P 500  
- Compare penalized regression methods under realistic constraints  
- Evaluate replication performance using financial metrics such as tracking error, beta, correlation, and Jensen’s alpha  
- Ensure methodological transparency and reproducibility  

---

## ⚙️ Features  
- Sparse asset selection via Ridge, Lasso, Elastic Net, and Adaptive Lasso  
- Non-negativity constraints to reflect long-only portfolio strategies  
- Variable screening using DC-SIS for dimensionality reduction  
- Rolling-origin cross-validation to mitigate look-ahead bias  
- Comprehensive performance evaluation (tracking error, beta, information ratio, Jensen’s alpha)  
- Robust preprocessing: outlier adjustment, stationarity testing, and log-return calculation  

---

## 🧰 Tech Stack  
Language: R  
Libraries & Packages:  
tidyverse, tidyquant, xts, zoo, glmnet, VariableScreening, PerformanceAnalytics, urca, readxl, forecast, caret, fBasics

All analyses were conducted within the R statistical environment with specialized time-series and econometric toolkits.

---

## ⚙️ Installation  

Clone the repository and ensure required R packages are installed:

```bash
git clone https://github.com/floriancrochet/master-year1-thesis.git  
cd master-year1-thesis  
install.packages(c("tidyverse","glmnet","xts","PerformanceAnalytics","urca","VariableScreening"))
```

---

## 📚 Usage Example  

```r
# Example: Fit Adaptive Lasso with DC-SIS  
set.seed(2103)  
model <- dcsis_glmnet_function("adlasso_dcsis", grid)  
model$best_model_results
```

Additional reproducible examples are available in the analysis scripts and notebooks within the repository.

---

## 📂 Project Structure  

```
master-year1-thesis/  
│  
├── data/                # S&P 500 index and constituent datasets  
├── src/                 # Core R scripts for modeling  
├── notebooks/           # Exploratory analysis and visualizations  
├── results/             # Model outputs and performance tables  
├── figures/             # Generated plots and diagnostics  
├── requirements.txt     # Package dependencies  
└── README.md
```

---

## 📊 Results  
Empirical results show that Lasso and Elastic Net achieve the lowest tracking error, while Adaptive Lasso offers the best trade-off between sparsity and performance. Adaptive Lasso selects approximately 140 stocks while maintaining strong replication and superior risk-adjusted returns, as indicated by its Information Ratio and Jensen’s alpha.

Tracking correlations reach approximately 0.994 for non-DC-SIS models and 0.983 for DC-SIS models, confirming strong index replication accuracy.

---

## 🧠 References  
Key theoretical foundations and methodologies draw from:  
- Tibshirani (1996), Lasso Regression  
- Hastie, Tibshirani & Friedman (2009), The Elements of Statistical Learning  
- Shu et al. (2020), Adaptive Elastic Net for High-Dimensional Index Tracking  
- Hyndman & Athanasopoulos, Forecasting: Principles and Practice  

---

## 📜 License  
This project is released under the MIT License  
© 2025 Florian Crochet

---

## 👤 Author  
**Florian Crochet**  
[GitHub Profile](https://github.com/floriancrochet)

*Master 1 – Econometrics & Statistics, Applied Econometrics Track*

---

## 💬 Acknowledgments  
This project was supervised by Mr. Olivier Darné and benefited from academic guidance in time series analysis and financial econometrics.
