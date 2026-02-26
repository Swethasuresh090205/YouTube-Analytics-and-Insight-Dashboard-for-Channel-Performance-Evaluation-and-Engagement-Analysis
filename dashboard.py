import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

st.title("📊 YouTube Advanced Analytics Dashboard")

# Input Section
channel_id = st.text_input("Enter YouTube Channel ID")
if generate_clicked:
    from main import fetch_and_store

st.button("Generate Insights", key="generate_btn")
fetch_and_store(channel_id)

    conn = sqlite3.connect("youtube_data.db")
    df = pd.read_sql_query("SELECT * FROM videos", conn)

    if df.empty:
        st.error("No data found. Please fetch data first.")
    else:
        # KPIs
        total_views = df["views"].sum()
        total_likes = df["likes"].sum()
        total_comments = df["comments"].sum()
        avg_engagement = ((df["likes"] + df["comments"]) / df["views"]).mean()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Videos", len(df))
        col2.metric("Total Views", total_views)
        col3.metric("Total Likes", total_likes)
        col4.metric("Avg Engagement Rate", round(avg_engagement, 4))

        # Top 5 Viewed
        st.subheader("🔥 Top 5 Most Viewed Videos")
        top_views = df.sort_values("views", ascending=False).head(5)
        fig1 = px.bar(top_views, x="views", y="title", orientation="h")
        st.plotly_chart(fig1, use_container_width=True)

        # Engagement Chart
        st.subheader("📈 Engagement Rate Analysis")
        df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"]
        fig2 = px.scatter(df, x="views", y="engagement_rate",
                          size="likes", hover_name="title")
        st.plotly_chart(fig2, use_container_width=True)

        # Pie Chart (Likes vs Comments)
        st.subheader("🥧 Likes vs Comments Distribution")
        pie_data = pd.DataFrame({
            "Metric": ["Likes", "Comments"],
            "Count": [total_likes, total_comments]
        })
        fig3 = px.pie(pie_data, values="Count", names="Metric")
        st.plotly_chart(fig3, use_container_width=True)

        # Publishing Trend
        st.subheader("📅 Publishing Trend")
        trend = df.groupby("published_date").size().reset_index(name="count")
        fig4 = px.line(trend, x="published_date", y="count")
        st.plotly_chart(fig4, use_container_width=True)


    conn.close()

