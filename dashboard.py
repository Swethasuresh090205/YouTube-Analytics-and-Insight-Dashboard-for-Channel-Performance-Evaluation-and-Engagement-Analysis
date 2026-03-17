importimport streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="CreatorScope AI",
    page_icon="🔥",
    layout="wide"
)

# ------------------------------------------------
# RED / ORANGE THEME
# ------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
background: linear-gradient(135deg,#ff0000,#ff4d00,#ff8c00);
color:white;
}

[data-testid="stSidebar"]{
background: linear-gradient(180deg,#ff0000,#ff4d00,#ff8c00);
}

h1,h2,h3{
color:white;
font-weight:bold;
}

.stMetric{
background: rgba(255,255,255,0.12);
padding:20px;
border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# LOGO + TITLE
# ------------------------------------------------

# ------------------------------------------------
# LOGO + TITLE
# ------------------------------------------------

import os
from PIL import Image

logo_path = r"C:\Users\SWETHA\OneDrive\Desktop\youtube_project\logo.png"

col1, col2 = st.columns([1,5])

with col1:
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, width=130)

with col2:
    st.title("CreatorScope AI")
    st.subheader("AI‑Powered YouTube Analytics Platform")

# ------------------------------------------------
# PRODUCT DESCRIPTION
# ------------------------------------------------

st.markdown("## 🚀 What is CreatorScope AI")

st.write("""
CreatorScope AI is an **AI-powered YouTube analytics platform** designed to help creators grow faster.

The platform combines analytics, artificial intelligence, and machine learning to analyze channel performance and optimize content strategy.

Creators can discover viral trends, generate video ideas, optimize thumbnails, and predict video performance.
""")

# ------------------------------------------------
# FEATURES
# ------------------------------------------------

st.markdown("## ⚡ Core Features")

col1,col2,col3 = st.columns(3)

with col1:
    st.write("🤖 AI Video Idea Generator")
    st.write("🎯 AI Title Generator")
    st.write("📈 Viral Video Detector")

with col2:
    st.write("🧠 AI Thumbnail Score")
    st.write("📊 Channel Analytics Dashboard")
    st.write("📅 Smart Upload Strategy")

with col3:
    st.write("🌍 Global Creator Rankings")
    st.write("📉 Growth Prediction")
    st.write("📄 PDF Analytics Reports")

# ------------------------------------------------
# $1M STARTUP FEATURES
# ------------------------------------------------

st.markdown("## 💡 Advanced AI Features")

st.write("""
🔥 Viral Probability Predictor  
Predicts if a video has viral potential.

🔥 Competitor Strategy Detector  
Analyzes competitor channels and their upload strategy.

🔥 AI Thumbnail CTR Predictor  
Estimates click-through rate of thumbnails.

🔥 Global Creator Leaderboard  
Ranks channels by growth velocity.

🔥 Channel Health Score  
AI score for overall channel performance.
""")

# ------------------------------------------------
# YOUTUBE API
# ------------------------------------------------

API_KEY = "AIzaSyAuY3e8myHBdmvPzhbs9Fgh3BjVop8X8PQ"

def get_channel_id_from_url(url):
   
    if "@" in url:
        username = url.split("@")[-1]

        api = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={username}&key={API_KEY}"

        r = requests.get(api).json()

        if "items" in r and len(r["items"]) > 0:
            return r["items"][0]["snippet"]["channelId"]

    return None

def get_channel_videos(channel_id):
   
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=50"

    r = requests.get(url).json()

    videos = []

    if "items" not in r:
        return pd.DataFrame()

    for item in r["items"]:

        if item["id"]["kind"] == "youtube#video":

            vid = item["id"]["videoId"]

            stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={vid}&key={API_KEY}"

            stats = requests.get(stats_url).json()

            if "items" not in stats:
                continue

            s = stats["items"][0]["statistics"]

            videos.append({
                "video_id": vid,
                "title": item["snippet"]["title"],
                "published_date": item["snippet"]["publishedAt"],
                "views": int(s.get("viewCount", 0)),
                "likes": int(s.get("likeCount", 0)),
                "comments": int(s.get("commentCount", 0))
            })

    return pd.DataFrame(videos)
# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("📊 CreatorScope Tools")

section = st.sidebar.radio(
"Navigation",
[
"Overview",
"Growth Analytics",
"Top Videos",
"Viral Detector",
"Upload Strategy",
"AI Keyword Insights",
"AI Video Ideas",
"AI Title Generator",
"Video Prediction",
"Thumbnail Generator",
"Thumbnail Score",
"Download Report"
]
)

youtube_url = st.sidebar.text_input("Enter YouTube Channel URL")

# ------------------------------------------------
# ANALYZE CHANNEL
# ------------------------------------------------

# ------------------------------------------------
# ANALYZE CHANNEL
# ------------------------------------------------

if st.sidebar.button("Analyze Channel"):

    if youtube_url == "":
        st.error("Please paste a YouTube Channel URL")
        st.stop()

    # Convert URL → Channel ID
    channel_id = get_channel_id_from_url(youtube_url)

    if channel_id is None:
        st.error("Could not find channel ID from URL")
        st.stop()

    # Fetch videos
    df = get_channel_videos(channel_id)

    if df.empty:
        st.error("No videos found or API error")
        st.stop()

    df["published_date"] = pd.to_datetime(df["published_date"])
    df["engagement"] = ((df["likes"] + df["comments"]) / df["views"]) * 100

# ------------------------------------------------
# OVERVIEW
# ------------------------------------------------

    if section == "Overview":

        st.header("📊 Channel Overview")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Videos",len(df))
        c2.metric("Total Views",int(df["views"].sum()))
        c3.metric("Total Likes",int(df["likes"].sum()))
        c4.metric("Comments",int(df["comments"].sum()))

# ------------------------------------------------
# GROWTH ANALYTICS
# ------------------------------------------------

    if section == "Growth Analytics":

        monthly = df.groupby(df["published_date"].dt.to_period("M"))["views"].sum().reset_index()

        monthly["published_date"] = monthly["published_date"].astype(str)

        fig = px.line(monthly,x="published_date",y="views",markers=True)

        st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# TOP VIDEOS
# ------------------------------------------------

    if section == "Top Videos":

        top = df.sort_values(by="views",ascending=False).head(10)

        fig = px.bar(top,x="views",y="title",orientation="h")

        st.plotly_chart(fig,use_container_width=True)

        st.dataframe(top)

# ------------------------------------------------
# VIRAL DETECTOR
# ------------------------------------------------

    if section == "Viral Detector":

        avg = df["views"].mean()

        viral = df[df["views"] > avg * 3]

        st.dataframe(viral)

# ------------------------------------------------
# AI KEYWORDS
# ------------------------------------------------

    if section == "AI Keyword Insights":

        words = " ".join(df["title"]).lower().split()

        stop = ["the","a","and","of","to","in"]

        words = [w for w in words if w not in stop]

        keywords = Counter(words).most_common(10)

        st.dataframe(pd.DataFrame(keywords,columns=["Keyword","Count"]))

# ------------------------------------------------
# AI VIDEO IDEAS
# ------------------------------------------------

    if section == "AI Video Ideas":

        topic = st.text_input("Channel Topic")

        if st.button("Generate Ideas"):

            ideas = [
            f"Top 10 {topic} Tips",
            f"{topic} Mistakes Beginners Make",
            f"I Tried {topic} for 30 Days",
            f"Ultimate {topic} Guide",
            f"{topic} Secrets Nobody Tells You"
            ]

            for i in ideas:
                st.write("🔥",i)

# ------------------------------------------------
# TITLE GENERATOR
# ------------------------------------------------

    if section == "AI Title Generator":

        topic = st.text_input("Video Topic")

        if st.button("Generate Titles"):

            titles = [
            f"{topic} Secrets You Must Know",
            f"I Tried {topic} for 7 Days",
            f"{topic} Beginner Guide",
            f"{topic} Challenge"
            ]

            for t in titles:
                st.write("👉",t)

# ------------------------------------------------
# VIDEO PREDICTION
# ------------------------------------------------

    if section == "Video Prediction":

        model = LinearRegression()

        X = df[["likes","comments"]]
        y = df["views"]

        model.fit(X,y)

        likes = st.number_input("Expected Likes")
        comments = st.number_input("Expected Comments")

        if st.button("Predict Views"):

            pred = model.predict([[likes,comments]])

            st.success(int(pred[0]))

# ------------------------------------------------
# THUMBNAIL GENERATOR
# ------------------------------------------------

    if section == "Thumbnail Generator":

        text = st.text_input("Thumbnail Text")

        if st.button("Generate"):

            url = f"https://dummyimage.com/1280x720/ff4d00/ffffff&text={text}"

            img = Image.open(BytesIO(requests.get(url).content))

            st.image(img)

# ------------------------------------------------
# THUMBNAIL SCORE
# ------------------------------------------------

    if section == "Thumbnail Score":

        file = st.file_uploader("Upload Thumbnail")

        if file:

            img = Image.open(file)

            img_np = np.array(img)

            gray = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)

            brightness = np.mean(gray)
            contrast = gray.std()

            score = (brightness + contrast) / 2

            st.image(img)

            st.success(f"Thumbnail Score: {round(score,2)}")

# ------------------------------------------------
# REPORT
# ------------------------------------------------

    if section == "Download Report":

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial",size=12)

        pdf.cell(200,10,"CreatorScope AI Report",ln=True)

        pdf.cell(200,10,f"Total Videos {len(df)}",ln=True)

        pdf.cell(200,10,f"Total Views {df['views'].sum()}",ln=True)

        pdf.cell(200,10,f"Avg Engagement {df['engagement'].mean()}",ln=True)

        pdf.output("report.pdf")

        with open("report.pdf","rb") as f:

            st.download_button(
                "Download Report",
                f,
                file_name="CreatorScope_Report.pdf"
            )
