import sqlite3
from googleapiclient.discovery import build

# 🔑 Your API Key
API_KEY = "AIzaSyAuY3e8myHBdmvPzhbs9Fgh3BjVop8X8PQ"

# 🔗 Connect to YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)


def fetch_and_store(channel_id):
    # 📥 Fetch most popular videos
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="US",
        maxResults=10
    )

    response = request.execute()

    # 🗄️ Connect to SQLite DB
    conn = sqlite3.connect("youtube_data.db")
    cursor = conn.cursor()

    # 📊 Insert data into table
    for item in response["items"]:
        video_id = item["id"]
        title = item["snippet"]["title"]
        published = item["snippet"]["publishedAt"]

        views = int(item["statistics"].get("viewCount", 0))
        likes = int(item["statistics"].get("likeCount", 0))
        comments = int(item["statistics"].get("commentCount", 0))

        cursor.execute("""
        INSERT OR REPLACE INTO videos
        (video_id, title, views, likes, comments, published_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (video_id, title, views, likes, comments, published))

    conn.commit()
    conn.close()

    print("YouTube data stored successfully!")


# ▶️ Run directly
if __name__ == "__main__":
    fetch_and_store("dummy_channel")
