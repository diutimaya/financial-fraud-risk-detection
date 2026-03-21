import os
import zipfile
import pandas as pd
import joblib
import streamlit as st

BASE = os.path.dirname(os.path.dirname(__file__))

def download_dataset():
    data_path = os.path.join(BASE, "data", "creditcard.csv")

    # If already downloaded, skip
    if os.path.exists(data_path):
        return data_path

    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)

    # Kaggle credentials from Streamlit secrets
    os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"]      = st.secrets["KAGGLE_KEY"]

    import kaggle
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "mlg-ulb/creditcardfraud",
        path=os.path.join(BASE, "data"),
        unzip=True
    )
    return data_path

def load_data():
    path = download_dataset()
    return pd.read_csv(path)

def load_model():
    path = os.path.join(BASE, "models", "fraud_detection_model.pkl")
    return joblib.load(path)

def get_risk_tier(prob):
    if prob > 0.75:
        return " High Risk"
    elif prob > 0.40:
        return " Medium Risk"
    else:
        return " Low Risk"


