from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()
model = joblib.load('./data/model.joblib')
scaler_income = joblib.load('./data/scaler_income.joblib')
scaler_age = joblib.load('./data/scaler_age.joblib')

AGE_INPUT_COL = getattr(scaler_age, 'feature_names_in_', np.array(['age']))[0]
INCOME_INPUT_COL = getattr(scaler_income, 'feature_names_in_', np.array(['income_log']))[0]

MODEL_FEATURES = [
    'Gender Code',
    'Marital Status Code',
    'Home Ownership Code',
    'Income log scaled',
    'Age scaled',
]

class CustomerData(BaseModel):
    age: int
    gender: str
    has_house: str
    marital_status: str
    income: float

def preprocess(data: CustomerData):
    gender_map = {'Male': 1, 'Female': -1}
    house_map = {'Owned': 1, 'Rented': -1}
    marital_map = {'Single': -1, 'Married': 1}

    age_df = pd.DataFrame({AGE_INPUT_COL: [data.age]})
    age_scaled = scaler_age.transform(age_df)[0, 0]

    income_log = np.log1p(data.income)
    income_df = pd.DataFrame({INCOME_INPUT_COL: [income_log]})
    income_log_scaled = scaler_income.transform(income_df)[0, 0]

    row = {
        'Gender Code': gender_map.get(data.gender, 0),
        'Marital Status Code': marital_map.get(data.marital_status, 0),
        'Home Ownership Code': house_map.get(data.has_house, 0),
        'Income log scaled': income_log_scaled,
        'Age scaled': age_scaled,
    }
    X = pd.DataFrame([row], columns=MODEL_FEATURES)
    return X


@app.post("/predict")
def predict(data: CustomerData):
    X = preprocess(data)
    y = int(model.predict(X)[0])
    label = "ACCEPTED" if y == 1 else "DENIED"
    return {"prediction": y, "label": label}