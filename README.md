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