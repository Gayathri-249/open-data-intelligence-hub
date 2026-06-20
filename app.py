import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Quality of Life Intelligence Platform",
    layout="wide"
)

st.title("🌍 Quality of Life Intelligence Platform")
st.markdown("Compare countries using World Happiness Report indicators.")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/world_happiness.csv")
    df.columns = df.columns.str.strip()  # remove hidden spaces
    return df

df = load_data()

# DEBUG (optional - remove later)
# st.write(df.columns)

# -----------------------------
# SAFE DATA PROCESSING
# -----------------------------
df_clean = pd.DataFrame()

# Required columns (World Happiness Report standard)
df_clean["Country"] = df["Country name"]

df_clean["Happiness"] = pd.to_numeric(df["Life Ladder"], errors="coerce")
df_clean["GDP"] = pd.to_numeric(df["Log GDP per capita"], errors="coerce")
df_clean["Social Support"] = pd.to_numeric(df["Social support"], errors="coerce")
df_clean["Health"] = pd.to_numeric(df["Healthy life expectancy at birth"], errors="coerce")
df_clean["Freedom"] = pd.to_numeric(df["Freedom to make life choices"], errors="coerce")
df_clean["Generosity"] = pd.to_numeric(df["Generosity"], errors="coerce")
df_clean["Corruption"] = pd.to_numeric(df["Perceptions of corruption"], errors="coerce")

# Remove rows with missing values
df_clean = df_clean.dropna()

# -----------------------------
# QoL SCORE CALCULATION
# -----------------------------
df_clean["QoL Score"] = (
    df_clean["Happiness"] * 0.30 +
    df_clean["GDP"] * 0.20 +
    df_clean["Health"] * 0.15 +
    df_clean["Freedom"] * 0.15 +
    df_clean["Social Support"] * 0.10 +
    df_clean["Generosity"] * 0.05 +
    df_clean["Corruption"] * 0.05
)

pdf = df_clean.copy()

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Country Comparison", "Top Rankings", "Analytics"]
)

# -----------------------------
# OVERVIEW PAGE
# -----------------------------
if page == "Overview":

    st.header("📊 Overview Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Countries", len(pdf))
    col2.metric("Avg QoL", round(pdf["QoL Score"].mean(), 2))
    col3.metric("Max QoL", round(pdf["QoL Score"].max(), 2))

    st.subheader("Dataset Preview")
    st.dataframe(pdf.head(50))

# -----------------------------
# COUNTRY COMPARISON
# -----------------------------
elif page == "Country Comparison":

    st.header("🌍 Country Comparison")

    countries = sorted(pdf["Country"].unique())

    c1 = st.selectbox("Select Country 1", countries)
    c2 = st.selectbox("Select Country 2", countries, index=1)

    compare_df = pdf[pdf["Country"].isin([c1, c2])]
    st.dataframe(compare_df)

    st.subheader("Comparison Metrics")

    metric_cols = [
        "GDP", "Health", "Freedom",
        "Social Support", "Generosity",
        "Corruption", "Happiness", "QoL Score"
    ]

    st.dataframe(compare_df.set_index("Country")[metric_cols])

# -----------------------------
# TOP RANKINGS
# -----------------------------
elif page == "Top Rankings":

    st.header("🏆 Top 10 Countries by QoL Score")

    top10 = pdf.sort_values("QoL Score", ascending=False).head(10)

    st.dataframe(top10)

    fig = px.bar(
        top10,
        x="Country",
        y="QoL Score",
        title="Top 10 Countries"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "Analytics":

    st.header("📈 Analytics Dashboard")

    fig1 = px.scatter(
        pdf,
        x="GDP",
        y="Happiness",
        hover_name="Country",
        title="GDP vs Happiness"
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.scatter(
        pdf,
        x="Freedom",
        y="Happiness",
        hover_name="Country",
        title="Freedom vs Happiness"
    )
    st.plotly_chart(fig2, use_container_width=True)

    top15 = pdf.sort_values("QoL Score", ascending=False).head(15)

    fig3 = px.bar(
        top15,
        x="Country",
        y="QoL Score",
        title="Top 15 Countries"
    )
    st.plotly_chart(fig3, use_container_width=True)

    corr = pdf[[
        "GDP", "Health", "Freedom",
        "Social Support", "Generosity",
        "Corruption", "Happiness", "QoL Score"
    ]].corr()

    fig4 = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Matrix"
    )

    st.plotly_chart(fig4, use_container_width=True)