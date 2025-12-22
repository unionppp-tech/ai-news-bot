import feedparser
from datetime import datetime

# 1. AI 뉴스 RSS (Google News)
RSS_URL = "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-US&gl=US&ceid=US:en"

feed = feedparser.parse(RSS_URL)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("===================================")
print("AI DAILY NEWS REPORT")
print(f"Generated at: {now}")
print("===================================\n")

# 2. 상위 5개 뉴스 출력
for i, entry in enumerate(feed.entries[:5], start=1):
    print(f"{i}. {entry.title}")
    print(f"   Link: {entry.link}\n")
