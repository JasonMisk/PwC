# PwC Data Science & Engineering Test Case

This repository contains the PwC Data Scientist/Engineer interview task. Within a 4-hour timeframe, analysis of Non-Performing Loan (NPL) ratios in banks relative to macroeconomic indicators will be performed, market share versus credit risk will be investigated, a basic ML model will be built, and an interactive UI will be delivered.

## Business Problems

1. Analysis of how NPL ratios in banks are affected by factors such as interest rates, inflation, unemployment, household debt to disposable income, and GDP growth.  
2. Investigation of the relationship between a bank’s market share, growth, and credit risk (proxied by NPL percentages) using BA900 data from the South African Reserve Bank.

## Tasks

1. **Data Extraction & Preprocessing**  
   - Scrape a subset of SARB BA900 data in Python, handle rate limits, and save raw CSV files.  
   - Clean for consistency and completeness (standardise date formats, handle missing values).

2. **Model Building**  
   - Conduct exploratory data analysis and feature selection.  
   - Build a simple ML model (e.g. linear regression) with time-series cross-validation.  
   - Interpret feature importances and validation metrics.

3. **UI Development**  
   - Develop a one-page app (Streamlit or similar) to visualise results interactively.

4. **Presentation Preparation**  
   - Create a concise slide deck or outline summarizing approach, findings, and recommendations.

---

### File Overview

- **sandbox/download_ba900.py**  
  Attempt to download BA900 data through the SARB API—XML parsing remains outstanding.

- **src/aggregate_credit_impairments.py**  
  Processes BA900 CSVs, extracts:
  - `Less: credit impairments in respect of loans and advances`  
  - `Overdrafts, loans and advances: private sector (items 181, 187, 188)`  
  and computes NPL ratios.

- **src/macro_totals_model.py**  
  Merges macroeconomic series with aggregated totals and fits a Decision Tree Regressor on NPL, printing evaluation metrics and feature importances.

- **src/macro_risk_dashboard.py**  
  A stub Streamlit “NPL Correlation Explorer” that visualises the correlation matrix between NPL and key macro indicators.

## Solution

- **Data Extraction & Preprocessing**  
  - Raw BA900 data collection framework in `sandbox/download_ba900.py`.  
  - Cleaned and aggregated credit-impairment series via `src/aggregate_credit_impairments.py`, producing the NPL target variable.

- **Model Building**  
  - Combined NPL with macro indicators in `src/macro_totals_model.py`.  
  - Trained and evaluated a Decision Tree Regressor, achieving reproducible MSE and R² scores, and surfaced key drivers via feature importances.

- **UI Development**  
  - Delivered `src/macro_risk_dashboard.py`, a Streamlit app stub (“NPL Correlation Explorer”) for interactive correlation analysis.

- **Next Steps**  
  - Finalise SARB XML parsing in `download_ba900.py`.  
  - Enhance model (e.g. incorporate time-series CV or ensemble methods).  
  - Build out slide deck with visualisations and actionable insights.

## Issues

- The method used to calculate NPL needs to be verified.  
- A more elegant, robust parser for BA900 XML/CSV files should be developed.  
- The macroeconomic data source may be outdated or inaccurate; identify and integrate a trusted, up-to-date source.  
- Additional data (longer time series, more granular series) would improve model performance.  
- Careful data preprocessing is required:  
  - Ensure correct aggregation of low-frequency predictors against the monthly NPL response.  
- Check for multicollinearity among predictors; if present, consider PCA or other dimensionality-reduction techniques.  
- The dashboard stub needs further development to support real data, interactivity, and styling.  
