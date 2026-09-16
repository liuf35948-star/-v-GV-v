import os
import requests
import re
from datetime import datetime

# ========== 修改这里 ==========
TARGET_URL = "https://example.com/target-page"
KEYWORDS = ["补货", "In Stock", "有货", "开售", "购买"]
# ==============================

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"发送失败: {e}")

def check():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get(TARGET_URL, headers=headers, timeout=15)
    text = resp.text
    status = resp.status_code

    # 提取标题
    title = ""
    m = re.search(r"<title>(.*?)</title>", text, re.I)
    if m:
        title = m.group(1).strip()

    # 匹配关键词
    matched = [kw for kw in KEYWORDS if kw in text]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if matched:
        msg = f"🔔 <b>发现关键词！</b>\n\n"
        msg += f"📌 匹配到: <code>{', '.join(matched)}</code>\n"
        msg += f"🔗 链接: {TARGET_URL}\n"
        msg += f"📄 标题: {title}\n"
        msg += f"📊 状态码: {status}\n"
        msg += f"🕐 时间: {now}"
        send_msg(msg)
        print(f"✅ 命中关键词: {matched}")
    else:
        print(f"ℹ️ 未命中关键词 | 状态码: {status} | {now}")

if __name__ == "__main__":
    check()

