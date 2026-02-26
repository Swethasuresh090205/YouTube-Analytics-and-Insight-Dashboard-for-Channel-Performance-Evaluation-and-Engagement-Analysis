import sqlite3

# Connect to database
conn = sqlite3.connect("youtube_data.db")
cursor = conn.cursor()

print("\n📊 YOUTUBE ANALYTICS REPORT\n")

# 1️⃣ Total Videos
cursor.execute("SELECT COUNT(*) FROM videos")
total_videos = cursor.fetchone()[0]
print(f"Total Videos: {total_videos}\n")

# 2️⃣ Top 5 Most Viewed Videos
print("🔥 Top 5 Most Viewed Videos:")
cursor.execute("""
    SELECT title, views
    FROM videos
    ORDER BY views DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    print(f"{row[0]} — {row[1]} views")
print()

# 3️⃣ Top 5 Most Liked Videos
print("👍 Top 5 Most Liked Videos:")
cursor.execute("""
    SELECT title, likes
    FROM videos
    ORDER BY likes DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    print(f"{row[0]} — {row[1]} likes")
print()

# 4️⃣ Engagement Rate Analysis
print("📈 Top 5 Engagement Rate Videos:")
cursor.execute("""
    SELECT title,
           ROUND((likes + comments) * 1.0 / views, 4) AS engagement_rate
    FROM videos
    WHERE views > 0
    ORDER BY engagement_rate DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    print(f"{row[0]} — Engagement Rate: {row[1]}")
print()

# 5️⃣ Posting Trend (Videos per Date)
print("📅 Posting Trend:")
cursor.execute("""
    SELECT published_date, COUNT(*)
    FROM videos
    GROUP BY published_date
    ORDER BY published_date
""")

for row in cursor.fetchall():
    print(f"{row[0]} — {row[1]} videos")

conn.close()