import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import pickle

# Load the data
data = pd.read_csv("C:\\Users\91810\Desktop\VJTI\Backend\htmlDetect\htmlDataset.csv")

# Prepare features and labels
X = data.drop('label', axis=1)
y = data['label']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train RandomForest model
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)

# Train XGBoost model
xgb_model = xgb.XGBClassifier()
xgb_model.fit(X_train, y_train)
with open('xgb_model.pkl', 'wb') as f:
    pickle.dump(xgb_model, f)

# Train LightGBM model
lgb_model = lgb.LGBMClassifier()
lgb_model.fit(X_train, y_train)
with open('lgb_model.pkl', 'wb') as f:
    pickle.dump(lgb_model, f)

# Train CatBoost model
cat_model = CatBoostClassifier(verbose=0)
cat_model.fit(X_train, y_train)
with open('cat_model.pkl', 'wb') as f:
    pickle.dump(cat_model, f)

# Save the scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
