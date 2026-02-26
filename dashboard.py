import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")
st.title("📊 YouTube Advanced Analytics Dashboard")

# Input
channel_id = st.text_input("Enter YouTube Channel ID")

# Button
generate_clicked = st.button("Generate Insights", key="generate_btn")

if generate_clicked:
    from main import fetch_and_store
    fetch_and_store(channel_id)

    conn = sqlite3.connect("youtube_data.db")
    df = pd.read_sql_query("SELECT * FROM videos", conn)

    if df.empty:
        st.error("No data found.")
    else:
        total_views = df["views"].sum()
        total_likes = df["likes"].sum()
        total_comments = df["comments"].sum()

        df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"]
        avg_engagement = df["engagement_rate"].mean()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Videos", len(df))
        col2.metric("Total Views", total_views)
        col3.metric("Total Likes", total_likes)
        col4.metric("Avg Engagement Rate", round(avg_engagement, 4))

    conn.close()
