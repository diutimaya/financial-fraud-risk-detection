import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import load_data, load_model, get_risk_tier

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="",import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from utils import load_data

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

st.set_page_config(
    page_title="FraudSentinel",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Syne:wght@400;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: #060810;
    color: #c9d1e0;
}

.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

/* ── Header ── */
.fs-header {
    display: flex;
    align-items: flex-end;
    gap: 16px;
    margin-bottom: 2rem;
    border-bottom: 1px solid #1a2035;
    padding-bottom: 1.5rem;
}
.fs-logo {
    font-family: 'Share Tech Mono', monospace;
    font-size: 32px;
    font-weight: 400;
    color: #ff4d4d;
    letter-spacing: -1px;
    line-height: 1;
}
.fs-logo span { color: #ff8c42; }
.fs-tagline {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #3a4a6b;
    margin-bottom: 4px;
}

/* ── Section label ── */
.fs-section {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #3a4a6b;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.fs-section::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1a2035;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #0c1120;
    border: 1px solid #1a2035;
    border-radius: 12px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover { border-color: #2a3a5a; transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.red::before   { background: linear-gradient(90deg, #ff4d4d, transparent); }
.kpi-card.amber::before { background: linear-gradient(90deg, #ff8c42, transparent); }
.kpi-card.green::before { background: linear-gradient(90deg, #22d17a, transparent); }
.kpi-card.blue::before  { background: linear-gradient(90deg, #4d9fff, transparent); }

.kpi-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3a4a6b;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 30px;
    font-weight: 400;
    line-height: 1;
    color: #e8edf5;
}
.kpi-card.red   .kpi-value { color: #ff4d4d; }
.kpi-card.amber .kpi-value { color: #ff8c42; }
.kpi-card.green .kpi-value { color: #22d17a; }
.kpi-card.blue  .kpi-value { color: #4d9fff; }
.kpi-sub {
    font-size: 11px;
    color: #3a4a6b;
    margin-top: 6px;
    font-family: 'Share Tech Mono', monospace;
}

/* ── Chart containers ── */
.chart-card {
    background: #0c1120;
    border: 1px solid #1a2035;
    border-radius: 12px;
    padding: 6px;
    margin-bottom: 12px;
}

hr { border-color: #1a2035 !important; margin: 1.5rem 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
df     = load_data()
fraud  = df[df['Class'] == 1]
normal = df[df['Class'] == 0]
fraud_rate = len(fraud) / len(df) * 100

# ── Plot theme helpers ─────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="#0c1120",
    plot_bgcolor="#0c1120",
    font_color="#6a7a9b",
    font_family="Share Tech Mono",
    margin=dict(t=40, b=20, l=20, r=20),
)

PLOT_AXES = dict(
    xaxis=dict(gridcolor="#1a2035", zeroline=False),
    yaxis=dict(gridcolor="#1a2035", zeroline=False),
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="fs-header">
    <div>
        <div class="fs-logo">Fraud<span>Sentinel</span></div>
        <div class="fs-tagline">Transaction Intelligence System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">Total Transactions</div>
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-sub">all time records</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Fraudulent</div>
        <div class="kpi-value">{len(fraud):,}</div>
        <div class="kpi-sub">flagged & blocked</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-label">Normal</div>
        <div class="kpi-value">{len(normal):,}</div>
        <div class="kpi-sub">cleared transactions</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">Fraud Rate</div>
        <div class="kpi-value">{fraud_rate:.2f}%</div>
        <div class="kpi-sub">of total volume</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Distribution ──────────────────────────────────────────────────────────────
st.markdown('<div class="fs-section">Distribution Analysis</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.3, 1.3])

with c1:
    fig_pie = go.Figure(go.Pie(
        values=[len(normal), len(fraud)],
        labels=["Normal", "Fraud"],
        hole=0.65,
        marker=dict(colors=["#22d17a", "#ff4d4d"], line=dict(color="#060810", width=3)),
        textinfo="percent",
        textfont=dict(family="Share Tech Mono", size=12, color="#c9d1e0"),
        hovertemplate="%{label}: %{value:,}<extra></extra>",
    ))
    fig_pie.add_annotation(
        text=f"{fraud_rate:.1f}%<br><span style='font-size:10px'>fraud</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="Share Tech Mono", size=18, color="#ff4d4d"),
    )
    fig_pie.update_layout(
        title=dict(text="Class Split", font=dict(size=13, color="#6a7a9b")),
        showlegend=True,
        legend=dict(font=dict(color="#6a7a9b", size=11)),
        height=280,
        **PLOT_LAYOUT,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    fig_amt = go.Figure()
    fig_amt.add_trace(go.Histogram(
        x=normal["Amount"], name="Normal", nbinsx=50,
        marker_color="#22d17a", opacity=0.75,
    ))
    fig_amt.add_trace(go.Histogram(
        x=fraud["Amount"], name="Fraud", nbinsx=50,
        marker_color="#ff4d4d", opacity=0.85,
    ))
    fig_amt.update_layout(
        barmode="overlay",
        title=dict(text="Amount Distribution", font=dict(size=13, color="#6a7a9b")),
        legend=dict(font=dict(color="#6a7a9b", size=11)),
        height=280,
        **PLOT_LAYOUT,
        **PLOT_AXES,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_amt, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        y=normal["Amount"], name="Normal",
        marker_color="#22d17a",
        line_color="#22d17a",
        fillcolor=hex_to_rgba("#22d17a", 0.13),
        boxmean=True,
    ))
    fig_box.add_trace(go.Box(
        y=fraud["Amount"], name="Fraud",
        marker_color="#ff4d4d",
        line_color="#ff4d4d",
        fillcolor=hex_to_rgba("#ff4d4d", 0.13),
        boxmean=True,
    ))
    fig_box.update_layout(
        title=dict(text="Amount Spread", font=dict(size=13, color="#6a7a9b")),
        legend=dict(font=dict(color="#6a7a9b", size=11)),
        height=280,
        **PLOT_LAYOUT,
        **PLOT_AXES,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Time Analysis ─────────────────────────────────────────────────────────────
st.markdown('<div class="fs-section">Temporal Patterns</div>', unsafe_allow_html=True)

df["Hour"] = (df["Time"] // 3600) % 24
hourly = df.groupby(["Hour", "Class"]).size().reset_index(name="Count")
hourly["Class"] = hourly["Class"].map({0: "Normal", 1: "Fraud"})

t1, t2 = st.columns([2, 1])

with t1:
    COLOR_MAP = {"Normal": "#22d17a", "Fraud": "#ff4d4d"}
    fig_time = go.Figure()
    for cls, color in COLOR_MAP.items():
        d = hourly[hourly["Class"] == cls]
        fig_time.add_trace(go.Scatter(
            x=d["Hour"], y=d["Count"], name=cls,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=5, color=color),
            fill="tozeroy",
            fillcolor=hex_to_rgba(color, 0.07),
        ))
    fig_time.update_layout(
        title=dict(text="Transactions by Hour of Day", font=dict(size=13, color="#6a7a9b")),
        legend=dict(font=dict(color="#6a7a9b", size=11)),
        height=260,
        **PLOT_LAYOUT,
        xaxis=dict(gridcolor="#1a2035", zeroline=False, tickmode="linear", dtick=2),
        yaxis=dict(gridcolor="#1a2035", zeroline=False),
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with t2:
    fraud_hourly = hourly[hourly["Class"] == "Fraud"].sort_values("Count", ascending=False).head(5)
    fig_peak = go.Figure(go.Bar(
        x=fraud_hourly["Count"],
        y=[f"Hour {int(h):02d}" for h in fraud_hourly["Hour"]],
        orientation="h",
        marker=dict(color="#ff4d4d", opacity=0.85),
        text=fraud_hourly["Count"],
        textposition="outside",
        textfont=dict(color="#6a7a9b", size=11, family="Share Tech Mono"),
    ))
    fig_peak.update_layout(
        title=dict(text="Peak Fraud Hours", font=dict(size=13, color="#6a7a9b")),
        height=260,
        **PLOT_LAYOUT,
        xaxis=dict(gridcolor="#1a2035", zeroline=False),
        yaxis=dict(gridcolor="#1a2035", zeroline=False, autorange="reversed"),
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_peak, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    layout="wide"
)

df = load_data()
model = load_model()
fraud = df[df['Class'] == 1]
normal = df[df['Class'] == 0]

# Fraud vs Normal Stats

st.title(" Fraud Detection Dashboard")
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

st.markdown("##  Live Transaction Prediction")
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
