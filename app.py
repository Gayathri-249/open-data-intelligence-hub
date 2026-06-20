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

st.markdown("""
Compare countries using World Happiness Report indicators
and analyze Quality of Life factors.
""")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/world_happiness.csv")

    # clean column names (VERY IMPORTANT)
    df.columns = df.columns.str.strip()

    return df


df = load_data()

# -----------------------------
# CHECK DATA LOADED
# -----------------------------
if df.empty:
    st.error("Dataset not loaded. Check CSV path inside /data folder.")
    st.stop()

# -----------------------------
# SAFE COLUMN MAPPING (FIXED)
# -----------------------------
rename_map = {
    "Country name": "Country",
    "Life Ladder": "Happiness Score",
    "Log GDP per capita": "GDP",
    "Social support": "Social Support",
    "Healthy life expectancy at birth": "Health",
    "Freedom to make life choices": "Freedom",
    "Generosity": "Generosity",
    "Perceptions of corruption": "Corruption"
}

df = df.rename(columns=rename_map)

# keep only required columns safely
required_cols = [
    "Country", "Happiness Score", "GDP",
    "Social Support", "Health",
    "Freedom", "Generosity", "Corruption"
]

df = df[[col for col in required_cols if col in df.columns]]

# remove missing values
df = df.dropna()

# -----------------------------
# QUALITY OF LIFE SCORE
# -----------------------------
df["QoL Score"] = (
    df["Happiness Score"] * 0.30 +
    df["GDP"] * 0.20 +
    df["Health"] * 0.15 +
    df["Freedom"] * 0.15 +
    df["Social Support"] * 0.10 +
    df["Generosity"] * 0.05 +
    df["Corruption"] * 0.05
)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Country Comparison", "Top Rankings", "Analytics"]
)

# -----------------------------
# OVERVIEW
# -----------------------------
if page == "Overview":

    st.header("📊 Overview Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Countries", len(df))
    col2.metric("Avg QoL Score", round(df["QoL Score"].mean(), 2))
    col3.metric("Max QoL Score", round(df["QoL Score"].max(), 2))

    st.subheader("Dataset Preview")
    st.dataframe(df.head(20))

# -----------------------------
# COUNTRY COMPARISON
# -----------------------------
elif page == "Country Comparison":

    st.header("🔍 Country Comparison")

    countries = df["Country"].dropna().unique()

    c1 = st.selectbox("Country 1", countries)
    c2 = st.selectbox("Country 2", countries, index=1)

    compare = df[df["Country"].isin([c1, c2])]

    st.dataframe(compare)

    st.subheader("Comparison Chart")

    fig = px.bar(
        compare.melt(id_vars="Country"),
        x="variable",
        y="value",
        color="Country",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TOP RANKINGS
# -----------------------------
elif page == "Top Rankings":

    st.header("🏆 Top Countries")

    top10 = df.sort_values("QoL Score", ascending=False).head(10)

    st.dataframe(top10)

    fig = px.bar(
        top10,
        x="Country",
        y="QoL Score"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "Analytics":

    st.header("📈 Analytics Dashboard")

    st.subheader("GDP vs Happiness")

    fig1 = px.scatter(
        df,
        x="GDP",
        y="Happiness Score",
        hover_name="Country"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Freedom vs Happiness")

    fig2 = px.scatter(
        df,
        x="Freedom",
        y="Happiness Score",
        hover_name="Country"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Correlation Heatmap")

    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    fig3 = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)