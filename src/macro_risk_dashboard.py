import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="NPL Correlation Matrix", layout="wide")
st.title("Correlation Matrix: NPL & Macroeconomic Indicators")

# Data frequency note:
# Macro predictors update at different intervals (e.g., quarterly vs. monthly),
# while the response variable (NPL) is monthly. To align these series:
# 1. Aggregate NPL over each interval where a predictor remains constant (e.g., use the period average).
# 2. Compute correlations on the aligned dataset.
# This approach ensures meaningful correlation analysis, though more granular data
# and sophisticated alignment methods can improve robustness.

# Generate stub data (in place of actual data - limited time)
np.random.seed(42)
n = 100
data = {
    'NPL Rate': np.random.rand(n),
    'Interest Rate': np.random.rand(n),
    'Inflation Rate': np.random.rand(n),
    'Unemployment Rate': np.random.rand(n),
    'Household Debt to Disposable Income': np.random.rand(n),
    'GDP Growth': np.random.rand(n)
}
df = pd.DataFrame(data)

# Calculate correlation matrix
corr_matrix = df.corr()

# Plot correlation matrix
fig = px.imshow(
    corr_matrix,
    text_auto=True,
    aspect="auto",
    title="Correlation Matrix of NPL and Macroeconomic Indicators"
)
st.plotly_chart(fig, use_container_width=True)
