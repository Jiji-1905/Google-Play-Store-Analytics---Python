import streamlit as st
import pandas as pd
import plotly.express as px
import os
os.listdir()
from google.colab import files
uploaded = files.upload()

st.title("Google Play Store Analytics Dashboard")

apps = pd.read_csv("Play Store Data.csv")
reviews = pd.read_csv("User Reviews.csv")

st.write(apps.head())

apps = apps.drop_duplicates()

apps['Installs'] = apps['Installs'].astype(str)
apps['Installs'] = apps['Installs'].str.replace('+', '', regex=False)
apps['Installs'] = apps['Installs'].str.replace(',', '', regex=False)
apps['Installs'] = pd.to_numeric(apps['Installs'], errors='coerce')

apps['Rating'] = pd.to_numeric(apps['Rating'], errors='coerce')
apps['Reviews'] = pd.to_numeric(apps['Reviews'], errors='coerce')

# SIDEBAR
st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Category",
    apps['Category'].dropna().unique()
)

filtered_df = apps[apps['Category'] == selected_category]

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Total Apps", len(filtered_df))

col2.metric(
    "Average Rating",
    round(filtered_df['Rating'].mean(), 2)
)

col3.metric(
    "Total Installs",
    int(filtered_df['Installs'].sum())
)

# SCATTER CHART
st.subheader("Rating vs Installs")

fig = px.scatter(
    filtered_df,
    x="Rating",
    y="Installs",
    size="Reviews",
    color="Category",
    hover_name="App"
)

st.plotly_chart(fig, use_container_width=True)

# DATA PREVIEW
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())
