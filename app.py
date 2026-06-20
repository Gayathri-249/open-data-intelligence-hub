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
Compare countries using World Happiness Report indicators and analyze Quality of Life factors.
""")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/world_happiness.csv")
    return df

df = load_data()

# -----------------------------
# CLEAN DATA (SAFE)
# -----------------------------
df = df.dropna()

# -----------------------------
# STANDARDIZE COLUMNS (SAFE CHECK)
# -----------------------------
df["Country"] = df["Country name"]
df["GDP"] = df["Log GDP per capita"]
df["Health"] = df["Healthy life expectancy"]
df["Freedom"] = df["Freedom to make life choices"]
df["Social Support"] = df["Social support"]
df["Generosity"] = df["Generosity"]
df["Corruption"] = df["Perceptions of corruption"]
df["Happiness Score"] = df["Life Ladder"]

# -----------------------------
# QoL SCORE
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
# SIDEBAR
# -----------------------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Country Comparison", "Top Rankings", "Analytics"]
)

# -----------------------------
# OVERVIEW
# -----------------------------
if page == "Overview":

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Countries", df["Country"].nunique())
    col2.metric("Avg QoL", round(df["QoL Score"].mean(), 2))
    col3.metric("Records", len(df))

    st.dataframe(df.head(20))

# -----------------------------
# COUNTRY COMPARISON
# -----------------------------
elif page == "Country Comparison":

    st.header("Country Comparison")

    countries = sorted(df["Country"].unique())

    c1 = st.selectbox("Country 1", countries)
    c2 = st.selectbox("Country 2", countries, index=1)

    compare = df[df["Country"].isin([c1, c2])]

    st.dataframe(compare)

# -----------------------------
# TOP RANKINGS
# -----------------------------
elif page == "Top Rankings":

    st.header("Top 10 Countries")

    top10 = df.sort_values("QoL Score", ascending=False).head(10)

    st.dataframe(top10)

    fig = px.bar(top10, x="Country", y="QoL Score")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "Analytics":

    st.header("Analytics")

    fig1 = px.scatter(df, x="GDP", y="Happiness Score", hover_name="Country")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.scatter(df, x="Freedom", y="Happiness Score", hover_name="Country")
    st.plotly_chart(fig2, use_container_width=True)

    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()

    fig3 = px.imshow(corr, text_auto=True, title="Correlation Matrix")
    st.plotly_chart(fig3, use_container_width=True)