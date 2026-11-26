
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="World Happiness Report",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 World Happiness Dashboard")

st.caption("Source: World Happiness Report 2023 | Kaggle")

# =====================================
# LOAD DATA
# =====================================

DATA = Path(__file__).parent / "world_happiness_2023.csv"

df = pd.read_csv(DATA)

df.columns = [
    "Country", "Region", "Score", "GDP",
    "Social_Support", "Life_Expectancy",
    "Freedom", "Generosity", "Corruption"
]

# =====================================
# SIDEBAR FILTERS
# =====================================

with st.sidebar:

    st.header("Filters")

    regions = ["All Regions"] + sorted(
        df["Region"].unique().tolist()
    )

    selected_region = st.selectbox(
        "Region", regions
    )

    top_n = st.slider(
        "Show top N countries", 5, 25, 15
    )

# Filter data by selected region

filtered = (
    df if selected_region == "All Regions"
    else df[df["Region"] == selected_region]
)

top = filtered.nlargest(
    top_n, "Score"
).sort_values("Score")

# =====================================
# KPI METRICS
# =====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries",
    len(filtered)
)

col2.metric(
    "Avg Score",
    f"{filtered['Score'].mean():.2f}",
    f"{filtered['Score'].mean() - df['Score'].mean():+.2f} vs global"
)

col3.metric(
    "Happiest",
    filtered.nlargest(1, "Score")["Country"].values[0]
)

st.divider()

# =====================================
# CHART 1: PROFESSOR DINA'S CHART
# =====================================

fig1 = px.bar(
    top,
    x="Score",
    y="Country",
    orientation="h",
    labels={
        "Score": "Happiness Score (0–10)",
        "Country": ""
    },
    template="plotly_white",
    title=f"Happiest {len(top)} Countries - {selected_region}",
    height=600
)

fig1.update_layout(
    xaxis=dict(range=[0, 8.0])
)

st.plotly_chart(fig1, width="stretch")

st.divider()

# =====================================
# CHART 2: MY CLASS EXERCISE
# =====================================

st.header("Happiness Compared to the Global Average")

st.write(
    "This chart compares each country's happiness "
    "score with the global average. Red represents "
    "below-average happiness and green represents "
    "above-average happiness."
)

# Calculate global average

global_average = df["Score"].mean()

# Calculate happiness difference

comparison = filtered.copy()

comparison["Difference"] = (
    comparison["Score"] - global_average
)

comparison = comparison.sort_values("Difference")

# Set a symmetric colour range

max_difference = (
    df["Score"] - global_average
).abs().max()

# Create diverging bar chart

fig2 = px.bar(
    comparison,
    x="Difference",
    y="Country",
    orientation="h",
    color="Difference",
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    range_color=[-max_difference, max_difference],
    title=f"Happiness Gap - {selected_region}",
    labels={
        "Difference": "Difference from Global Average",
        "Country": ""
    },
    template="plotly_white",
    height=max(500, len(comparison) * 22)
)

# Annotate the midpoint

fig2.add_vline(
    x=0,
    line_dash="dash",
    line_color="gray",
    annotation_text=f"Global average: {global_average:.2f}",
    annotation_position="top"
)

# Display second chart

st.plotly_chart(fig2, width="stretch")

st.divider()

st.caption("Built with Streamlit + Plotly")
