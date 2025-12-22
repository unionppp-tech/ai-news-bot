import feedparser
from datetime import datetime
import os

# 🇰🇷 한국 AI 뉴스 RSS (Google News)
RSS_URL = "https://news.google.com/rss/search?q=인공지능+OR+AI&hl=ko&gl=KR&ceid=KR:ko"

feed = feedparser.parse(RSS_URL)

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

# 결과 저장 폴더
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file_path = f"{OUTPUT_DIR}/ai_news_kr_{date_str}.md"

lines = []
lines.append(f"# 🇰🇷 AI 데일리 뉴스 ({date_str})\n")
lines.append(f"_생성 시각: {time_str}_\n")

# 상위 5개 한국 AI 뉴스
for i, entry in enumerate(feed.entries[:5], start=1):
    lines.append(f"## {i}. {entry.title}")
    lines.append(f"- 🔗 링크: {entry.link}\n")

content = "\n".join(lines)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved Korean AI news report to {file_path}")
