import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Quality of Life Intelligence Platform", layout="wide")

st.title("🌍 Quality of Life Intelligence Platform")

st.markdown("Compare countries using World Happiness Report indicators.")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/world_happiness.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

if df.empty:
    st.error("Dataset not loaded")
    st.stop()

# -----------------------------
# SAFE COLUMN HANDLING (IMPORTANT FIX)
# -----------------------------
# detect correct columns automatically
def get_col(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

country_col = get_col(["Country name", "Country"])
gdp_col = get_col(["Log GDP per capita"])
life_col = get_col(["Life Ladder", "Happiness Score"])
social_col = get_col(["Social support"])
health_col = get_col(["Healthy life expectancy at birth"])
freedom_col = get_col(["Freedom to make life choices"])
generosity_col = get_col(["Generosity"])
corruption_col = get_col(["Perceptions of corruption"])

# -----------------------------
# BUILD CLEAN DATAFRAME
# -----------------------------
data = pd.DataFrame()

data["Country"] = df[country_col]

data["Happiness"] = df[life_col] if life_col else 0
data["GDP"] = df[gdp_col] if gdp_col else 0
data["Social Support"] = df[social_col] if social_col else 0
data["Health"] = df[health_col] if health_col else 0
data["Freedom"] = df[freedom_col] if freedom_col else 0
data["Generosity"] = df[generosity_col] if generosity_col else 0
data["Corruption"] = df[corruption_col] if corruption_col else 0

data = data.dropna()

# -----------------------------
# QoL SCORE
# -----------------------------
data["QoL Score"] = (
    data["Happiness"] * 0.30 +
    data["GDP"] * 0.20 +
    data["Health"] * 0.15 +
    data["Freedom"] * 0.15 +
    data["Social Support"] * 0.10 +
    data["Generosity"] * 0.05 +
    data["Corruption"] * 0.05
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

    st.header("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Countries", len(data))
    col2.metric("Avg QoL", round(data["QoL Score"].mean(), 2))
    col3.metric("Max QoL", round(data["QoL Score"].max(), 2))

    st.dataframe(data.head(20))

# -----------------------------
# COUNTRY COMPARISON
# -----------------------------
elif page == "Country Comparison":

    st.header("🔍 Compare Countries")

    countries = data["Country"].dropna().unique()

    c1 = st.selectbox("Country 1", countries)
    c2 = st.selectbox("Country 2", countries, index=1)

    compare = data[data["Country"].isin([c1, c2])]
    st.dataframe(compare)

    fig = px.bar(
        compare.melt(id_vars="Country"),
        x="variable",
        y="value",
        color="Country",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TOP RANKING
# -----------------------------
elif page == "Top Rankings":

    st.header("🏆 Top Countries")

    top10 = data.sort_values("QoL Score", ascending=False).head(10)

    st.dataframe(top10)

    fig = px.bar(top10, x="Country", y="QoL Score")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "Analytics":

    st.header("📈 Analytics")

    fig1 = px.scatter(
        data,
        x="GDP",
        y="Happiness",
        hover_name="Country"
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.scatter(
        data,
        x="Freedom",
        y="Happiness",
        hover_name="Country"
    )
    st.plotly_chart(fig2, use_container_width=True)

    corr = data.select_dtypes(include="number").corr()

    fig3 = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)