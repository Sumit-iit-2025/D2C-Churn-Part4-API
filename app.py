from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pickle
import pandas as pd
import os

app = FastAPI(title="Churn Prediction API", version="1.0")

MODEL_PATH = "model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model_artifact = pickle.load(f)
        model = model_artifact["model"]
        expected_features = model_artifact["features"]
except Exception as e:
    model = None
    expected_features = []
    print(f"Warning: Model not found at {MODEL_PATH}. Error: {e}")

class CustomerData(BaseModel):
    customer_id: str
    features: Dict[str, float]

class BatchCustomerData(BaseModel):
    customers: List[CustomerData]

@app.get("/health")
def health_check():
    if model is None:
        return {"status": "degraded", "message": "Model not loaded properly."}
    return {"status": "ok"}

def process_prediction(data: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    df = pd.DataFrame([data.features])
    
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0.0
            
    df = df[expected_features]
    
    # Predicting using the custom threshold of 0.35 from Part 3
    prob = float(model.predict_proba(df)[0, 1])
    pred_class = int(prob >= 0.35) 
    
    risk_level = "high" if pred_class == 1 else "low"
    explanation = "Elevated churn risk detected based on recent behavioral and transactional signals." if pred_class == 1 else "Customer exhibits stable retention signals."
    
    return {
        "customer_id": data.customer_id,
        "churn_probability": round(prob, 4),
        "predicted_class": pred_class,
        "risk_level": risk_level,
        "risk_explanation": explanation
    }

@app.post("/predict")
def predict(data: CustomerData):
    return process_prediction(data)

@app.post("/batch_predict")
def batch_predict(data: BatchCustomerData):
    results = [process_prediction(cust) for cust in data.customers]
    return {"predictions": results}
