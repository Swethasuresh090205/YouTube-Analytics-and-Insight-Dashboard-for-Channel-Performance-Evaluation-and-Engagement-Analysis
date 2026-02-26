import sqlite3

conn = sqlite3.connect("youtube_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    published_date TEXT
)
""")

conn.commit()
conn.close()

print("Table created successfully!")
