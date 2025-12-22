import feedparser
from datetime import datetime
import os

# RSS
RSS_URL = "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-US&gl=US&ceid=US:en"
feed = feedparser.parse(RSS_URL)

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

# 저장 폴더
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file_path = f"{OUTPUT_DIR}/ai_news_{date_str}.md"

lines = []
lines.append(f"# AI Daily News ({date_str})\n")
lines.append(f"_Generated at {time_str}_\n")

for i, entry in enumerate(feed.entries[:5], start=1):
    lines.append(f"## {i}. {entry.title}")
    lines.append(f"- Link: {entry.link}\n")

content = "\n".join(lines)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved report to {file_path}")
