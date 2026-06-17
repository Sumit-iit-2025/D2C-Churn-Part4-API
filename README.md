# FastAPI Churn Scoring Service

This repository contains a RESTful API built with FastAPI that serves the D2C Customer Churn Prediction model. 

## Setup & Reproducibility Instructions

```bash
git clone [https://github.com/Sumit-iit-2025/D2C-Churn-Part4-API.git]
cd D2C-Churn-Part4-API
pip install -r requirement.txt
uvicorn app.main:app --reload
pytest test_api.py
