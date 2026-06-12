import requests
import hashlib
import os

PUSH_TOKEN = os.getenv("PUSH_TOKEN")
TARGET_URL = os.getenv("TARGET_URL")

if not PUSH_TOKEN or not TARGET_URL:
    print("ERROR：环境变量读取为空，请检查GitHub Secrets配置")
    exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    resp = requests.get(TARGET_URL, headers=headers, timeout=15)
    resp.raise_for_status()
    html = resp.text
except Exception as e:
    print(f"网页抓取失败：{str(e)}")
    exit(1)

new_hash = hashlib.md5(html.encode("utf-8")).hexdigest()
record_file = "hash_record.txt"
old_hash = ""

if os.path.exists(record_file):
    with open(record_file, "r", encoding="utf-8") as f:
        old_hash = f.read().strip()

if new_hash != old_hash:
    push_url = f"https://xizhi.qqoq.net/{PUSH_TOKEN}.send?title=江苏考试院页面更新提醒&content=招考页面内容发生变动，请手动访问官网查看最新公告"
    try:
        requests.get(push_url, timeout=10)
        print("页面更新，已发送微信推送")
    except Exception as e:
        print(f"推送接口调用失败：{str(e)}")
    with open(record_file, "w", encoding="utf-8") as f:
        f.write(new_hash)
else:
    print("页面无更新，无需推送")
