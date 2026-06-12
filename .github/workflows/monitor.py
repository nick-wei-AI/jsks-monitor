import requests
import hashlib
import os

# 从GitHub Secrets读取配置，不用硬编码密钥
PUSH_TOKEN = os.getenv("PUSH_TOKEN")
TARGET_URL = os.getenv("TARGET_URL")

# 1. 抓取页面
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
resp = requests.get(TARGET_URL, headers=headers, timeout=15)
resp.raise_for_status()
html = resp.text

# 2. 计算页面哈希
new_hash = hashlib.md5(html.encode("utf-8")).hexdigest()
record_file = "hash_record.txt"

# 3. 读取历史哈希
old_hash = ""
if os.path.exists(record_file):
    with open(record_file, "r", encoding="utf-8") as f:
        old_hash = f.read().strip()

# 4. 比对，不一致推送微信
if new_hash != old_hash:
    # 组装息知推送链接
    push_url = f"https://xizhi.qqoq.net/{PUSH_TOKEN}.send?title=江苏考试院页面更新提醒&content=招考页面内容发生变动，请手动访问官网查看最新公告"
    requests.get(push_url, timeout=10)
    # 写入新哈希
    with open(record_file, "w", encoding="utf-8") as f:
        f.write(new_hash)
else:
    print("页面无更新，无需推送")
