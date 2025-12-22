import feedparser
from datetime import datetime
import os
import re

# 🇰🇷 한국 AI 뉴스 RSS
RSS_URL = "https://news.google.com/rss/search?q=인공지능+OR+AI&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(RSS_URL)

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

file_path = f"{OUTPUT_DIR}/ai_news_kr_{date_str}.md"

def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)   # HTML 제거
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def simple_summary(title: str, desc: str) -> str:
    """
    매우 안정적인 규칙 기반 요약
    - 제목 + 설명 일부 조합
    - 최대 2문장
    """
    desc = clean_text(desc)

    if not desc:
        return f"{title} 관련 소식이다."

    sentences = re.split(r"[.!?。]", desc)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if len(sentences) == 0:
        return desc[:120] + "..."

    if len(sentences) == 1:
        return sentences[0]

    return sentences[0] + ". " + sentences[1]

lines = []
lines.append(f"# 🇰🇷 AI 데일리 뉴스 ({date_str})\n")
lines.append(f"_생성 시각: {time_str}_\n")

# 상위 5개 뉴스 + 요약
for i, entry in enumerate(feed.entries[:5], start=1):
    title = entry.title
    desc = entry.get("summary", "")

    summary = simple_summary(title, desc)

    lines.append(f"## {i}. {title}")
    lines.append(f"- 🧠 요약: {summary}")
    lines.append(f"- 🔗 링크: {entry.link}\n")

content = "\n".join(lines)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved Korean AI news report with summary to {file_path}")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# 이메일 발송
email_subject = f"[AI 데일리 뉴스] {date_str}"
send_email(email_subject, content)

print("Email sent successfully")

import requests
import json

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_to_discord(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("No DISCORD_WEBHOOK_URL set")
        return

    payload = {
        "content": message[:1900]  # 디스코드 메시지 길이 제한
    }

    r = requests.post(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=10
    )

    if r.status_code == 204:
        print("Discord message sent")
    else:
        print(f"Discord send failed: {r.status_code}, {r.text}")

# 🔔 디스코드로 뉴스 전송
send_to_discord(content)


