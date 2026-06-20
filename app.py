import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG
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
    return pd.read_csv("data/world_happiness.csv")

df = load_data()

# -----------------------------
# CLEAN COLUMN NAMES (IMPORTANT FIX)
# -----------------------------
df.columns = df.columns.str.strip()

st.sidebar.subheader("Dataset Columns")
st.sidebar.write(df.columns.tolist())

# -----------------------------
# RENAME COLUMNS (BASED ON YOUR DATA)
# -----------------------------
df = df.rename(columns={
    "Country name": "Country",
    "Life evaluation (3-year average)": "Happiness Score",
    "Explained by: Log GDP per capita": "GDP",
    "Explained by: Social support": "Social Support",
    "Explained by: Healthy life expectancy": "Health",
    "Explained by: Freedom to make life choices": "Freedom",
    "Explained by: Generosity": "Generosity",
    "Explained by: Perceptions of corruption": "Corruption"
})

# -----------------------------
# REQUIRED CHECK (SAFE MODE)
# -----------------------------
required_cols = [
    "Country",
    "Happiness Score",
    "GDP",
    "Social Support",
    "Health",
    "Freedom",
    "Generosity",
    "Corruption"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# -----------------------------
# CLEAN DATA TYPES
# -----------------------------
for col in required_cols[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# -----------------------------
# QoL SCORE CALCULATION
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

    st.header("Overview Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Countries", df["Country"].nunique())
    col2.metric("Avg QoL", round(df["QoL Score"].mean(), 2))
    col3.metric("Top Country", df.sort_values("QoL Score", ascending=False).iloc[0]["Country"])
    col4.metric("Lowest Country", df.sort_values("QoL Score").iloc[0]["Country"])

    st.dataframe(df)

# -----------------------------
# COUNTRY COMPARISON
# -----------------------------
elif page == "Country Comparison":

    st.header("Country Comparison")

    countries = sorted(df["Country"].unique())

    c1 = st.selectbox("Select Country 1", countries)
    c2 = st.selectbox("Select Country 2", countries, index=1)

    comp_df = df[df["Country"].isin([c1, c2])]

    st.dataframe(comp_df)

    st.subheader("Key Indicators Comparison")

    compare_cols = [
        "GDP", "Health", "Freedom",
        "Social Support", "Generosity",
        "Corruption", "Happiness Score", "QoL Score"
    ]

    st.dataframe(comp_df[compare_cols + ["Country"]].set_index("Country"))

# -----------------------------
# TOP RANKINGS
# -----------------------------
elif page == "Top Rankings":

    st.header("Top 10 Countries by QoL Score")

    top10 = df.sort_values("QoL Score", ascending=False).head(10)

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

    st.header("Analytics Dashboard")

    st.subheader("GDP vs Happiness Score")

    fig1 = px.scatter(
        df,
        x="GDP",
        y="Happiness Score",
        hover_name="Country"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Freedom vs Happiness Score")

    fig2 = px.scatter(
        df,
        x="Freedom",
        y="Happiness Score",
        hover_name="Country"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 15 Countries")

    top15 = df.sort_values("QoL Score", ascending=False).head(15)

    fig3 = px.bar(
        top15,
        x="Country",
        y="QoL Score"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Correlation Heatmap")

    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    fig4 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )
    st.plotly_chart(fig4, use_container_width=True)