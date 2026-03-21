import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import load_data, load_model, get_risk_tier

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)

df = load_data()
model = load_model()
fraud = df[df['Class'] == 1]
normal = df[df['Class'] == 0]

# Fraud vs Normal Stats

st.title(" Credit Card Fraud Detection Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(df):,}")
col2.metric("Fraudulent", f"{len(fraud):,}", delta= " Flagged")
col3.metric("Normal", f"{len(normal):,}")
col4.metric("Fraud Rate", f"{(len(fraud)/len(df)*100):.2f}%")

# Pie chart
fig_pie = px.pie(
    values=[len(normal), len(fraud)],
    names=["Normal", "Fraud"],
    color_discrete_sequence=["#00CC96", "#EF553B"],
    title="Transaction Class Distribution"
)
st.plotly_chart(fig_pie, use_container_width=True)

# Amount & Time Analysis

st.markdown("## Transaction Amount Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_amt = px.histogram(
        df, x="Amount", color=df["Class"].map({0:"Normal", 1:"Fraud"}),
        nbins=50, title="Amount Distribution by Class",
        color_discrete_map={"Normal":"#00CC96", "Fraud":"#EF553B"}
    )
    st.plotly_chart(fig_amt, use_container_width=True)

with col2:
    fig_box = px.box(
        df, x=df["Class"].map({0:"Normal",1:"Fraud"}),
        y="Amount", color=df["Class"].map({0:"Normal",1:"Fraud"}),
        title="Amount Spread: Fraud vs Normal",
        color_discrete_map={"Normal":"#00CC96","Fraud":"#EF553B"}
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("## Time-Based Fraud Patterns")

df["Hour"] = (df["Time"] // 3600) % 24
hourly = df.groupby(["Hour","Class"]).size().reset_index(name="Count")
hourly["Class"] = hourly["Class"].map({0:"Normal", 1:"Fraud"})

fig_time = px.line(
    hourly, x="Hour", y="Count", color="Class",
    title="Transactions by Hour of Day",
    color_discrete_map={"Normal":"#00CC96","Fraud":"#EF553B"}
)
st.plotly_chart(fig_time, use_container_width=True)

# Live Model Prediction

st.markdown("## 🔮 Live Transaction Prediction")
st.info("Enter transaction details to check if it's fraudulent.")

with st.form("prediction_form"):
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=100.0)
    time = st.number_input("Time (seconds since first transaction)", min_value=0.0, value=50000.0)

    st.markdown("**PCA Features (V1–V10) — paste from your data:**")
    cols = st.columns(5)
    v_vals = []
    for i in range(1, 29):
        col = cols[(i-1) % 5] if i <= 10 else None
        if i <= 10:
            v_vals.append(col.number_input(f"V{i}", value=0.0, key=f"v{i}"))
        else:
            v_vals.append(0.0)  # default rest to 0

    submitted = st.form_submit_button(" Predict")

if submitted:
    features = [time] + v_vals + [amount]
    prob = model.predict_proba([features])[0][1]
    risk = get_risk_tier(prob)

    st.markdown("### Result")
    col1, col2 = st.columns(2)
    col1.metric("Fraud Probability", f"{prob*100:.2f}%")
    col2.metric("Risk Level", risk)

    if prob > 0.75:
        st.error(" HIGH RISK — This transaction is likely fraudulent!")
    elif prob > 0.40:
        st.warning(" MEDIUM RISK — Review this transaction carefully.")
    else:
        st.success(" LOW RISK — Transaction appears normal.")