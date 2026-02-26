import sqlite3
from googleapiclient.discovery import build
def fetch_and_store(channel_id):
    # your existing API code here
    # store data into youtube_data.db
API_KEY = "AIzaSyAuY3e8myHBdmvPzhbs9Fgh3BjVop8X8PQ"

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Step 1: Get most popular videos
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="US",
    maxResults=10
)

response = request.execute()

# Step 2: Connect to database
conn = sqlite3.connect("youtube_data.db")
cursor = conn.cursor()

# Step 3: Insert data
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

