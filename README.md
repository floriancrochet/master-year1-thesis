# Index Tracking and Asset Selection  
*A research project on sparse index replication using penalized regression techniques for the S&P 500.*

---

## 📘 Overview
This project provides tools for **replicating the S&P 500 index using a sparse subset of its constituent stocks through penalized regression methods**.  
It was developed as part of a Master 1 dissertation in **Econometrics and Statistics (Applied Econometrics Track)**, focusing on **methodological rigor, model interpretability, and reproducibility**.

The study applies Ridge, Lasso, Elastic Net, and Adaptive Lasso regressions under non-negativity constraints to construct parsimonious portfolios that minimize tracking error while preserving replication accuracy.

**Objectives**
- Construct sparse portfolios that replicate S&P 500 returns  
- Identify stable subsets of assets using penalized regression  
- Evaluate replication performance via tracking and risk metrics  
- Provide a reproducible analytical framework for ETF design  

---

## ⚙️ Features
- Penalized regression with non-negativity constraints  
- Variable screening via Distance Correlation Sure Independence Screening (DC-SIS)  
- Rolling-origin cross-validation to prevent look-ahead bias  
- Comparative evaluation of Ridge, Lasso, Elastic Net, and Adaptive Lasso  
- Portfolio performance metrics: Tracking Error, Beta, Information Ratio, Jensen’s Alpha  
- Interactive results visualization through a dedicated dashboard  

---

## 🧰 Tech Stack
**Language:** R  
**Core packages:** glmnet, VariableScreening, xts, zoo, PerformanceAnalytics, urca  

**Visualization stack:** Python (Dash, Plotly, Pandas) for the results application

---

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/floriancrochet/master-year1-thesis.git
cd master-year1-thesis
```

---

## 📚 Usage Example

```r
# Example: Fit a penalized regression model with DC-SIS
model <- dcsis_glmnet_function("adlasso_dcsis", grid)

# Retrieve selected coefficients
coefficients <- model$model_coefs

# Count number of selected variables
nb_variables <- model$model_variables
```

> Additional examples can be found in the code repository and associated scripts.

---

## 📂 Project Structure

```
master-year1-thesis/
│
├── thesis.pdf                     # Full dissertation
├── thesis_code/                   # R code for econometric analysis
├── thesis_data_visualization/     # Dash application for results visualization
├── data/                          # Processed financial datasets (CSV)
├── assets/                        # Figures and charts
└── README.md
```

---

## 📊 Results
The empirical results demonstrate that:

- **Lasso and Elastic Net** achieve the lowest tracking error and highest replication accuracy.  
- **Adaptive Lasso** produces the most parsimonious portfolios and delivers superior risk-adjusted performance.  
- **DC-SIS** improves model stability but slightly increases tracking error due to aggressive dimensionality reduction.

The visualization application includes:
- Variable selection diagrams  
- Hyperparameter comparison charts  
- Coefficient tables by model  
- Portfolio performance graphs  

> Example visualization:  
> `thesis_data_visualization` dashboard presents comparative performance metrics and coefficient distributions.

---

## 🧠 References
- Zou (2006) – *The Adaptive Lasso and Its Oracle Properties*  
- Tibshirani (1996) – *Regression Shrinkage and Selection via the Lasso*  
- Wu & Yang (2014) – *Nonnegative Elastic Net for Index Tracking*  
- Székely et al. (2007) – *Measuring Dependence by Correlation of Distances*

---

## 📜 License
This project is released under the **MIT License**.  
© 2025 Florian Crochet

---

## 👤 Author
**Florian Crochet**  
[GitHub Profile](https://github.com/floriancrochet)

*Master 1 – Econometrics & Statistics, Applied Econometrics Track*

---

## 💬 Acknowledgments
This work was supervised by **Mr. Olivier Darné**.
