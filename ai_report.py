import feedparser
from datetime import datetime
import os
import requests

# 1. 한국 AI 뉴스 RSS
RSS_URL = "https://news.google.com/rss/search?q=인공지능+OR+AI&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(RSS_URL)

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
file_path = f"{OUTPUT_DIR}/ai_news_kr_{date_str}.md"

# 2. 요약 함수 (HuggingFace 무료)
def summarize(text):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    payload = {"inputs": text}

    try:
        r = requests.post(url, json=payload, timeout=10)

        # 상태 코드 체크
        if r.status_code != 200:
            return "요약 생략 (API 제한)"

        result = r.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]

        return "요약 생략 (응답 오류)"

    except Exception:
        return "요약 생략 (연결 실패)"

# 3. 상위 5개 뉴스 + 요약
for i, entry in enumerate(feed.entries[:5], start=1):
    title = entry.title
    desc = entry.get("summary", "")
    text_for_summary = f"{title}. {desc}"

    summary = summarize(text_for_summary)

    lines.append(f"## {i}. {title}")
    lines.append(f"- 🔗 링크: {entry.link}")
    lines.append(f"- 🧠 요약: {summary}\n")

content = "\n".join(lines)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved Korean AI news report to {file_path}")
