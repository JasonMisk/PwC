# Revised script without duplication, with clear structure

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load data
macro_path = '../data/macro_economic_data.csv'
totals_path = '../data/aggregated_totals.csv'

df_macro = pd.read_csv(macro_path, index_col=0, parse_dates=True)
df_totals = pd.read_csv(totals_path, index_col='date', parse_dates=True)

# 2. Combine and clean
df = df_macro.join(df_totals, how='outer')
df_clean = df.dropna()

# 3. Note on mixed frequencies:
#    Predictors update quarterly or less frequently,
#    response (NPL) updates monthly.
#    A decision tree can handle this asynchronously-updated data.

# 4. Define features (X) and target (y)
X = df_clean.drop(columns=['NPL'])
y = df_clean['NPL']

# 5. Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# 6. Initialize and fit the Decision Tree Regressor
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# 7. Make predictions and evaluate
y_pred = model.predict(X_test)
print(f"Test MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"Test R²: {r2_score(y_test, y_pred):.4f}")

# 8. Display feature importances
importances = pd.Series(model.feature_importances_, index=X.columns)\
                 .sort_values(ascending=False)
print("\nFeature Importances:")
print(importances.to_string())

# The model results are poor - the model is clearly overfitting. Better data pre-processing can be done,
# and even proper feature selection. More data would also assist in working around the low-frequency predictors.
# Also, the target can be downsampled (aggregated to a mean) to get to the predictors frequency.
