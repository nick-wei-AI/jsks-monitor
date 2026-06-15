import requests
import hashlib
import os

# 从环境变量读取两个网页的地址
PUSH_TOKEN = os.getenv("PUSH_TOKEN")
TARGET_URLS = [
    {"url": os.getenv("TARGET_URL"), "name": "江苏考试院招考信息"},
    {"url": os.getenv("TARGET_URL_2"), "name": "阳光高考-高考资讯"}
]

if not PUSH_TOKEN or not all(t["url"] for t in TARGET_URLS):
    print("ERROR：环境变量读取为空，请检查GitHub Secrets配置")
    exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for site in TARGET_URLS:
    url = site["url"]
    site_name = site["name"]
    record_file = f"hash_{site_name}.txt"

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        print(f"[{site_name}] 网页抓取失败：{str(e)}")
        continue

    new_hash = hashlib.md5(html.encode("utf-8")).hexdigest()
    old_hash = ""

    if os.path.exists(record_file):
        with open(record_file, "r", encoding="utf-8") as f:
            old_hash = f.read().strip()

    if new_hash != old_hash:
        push_url = f"https://xizhi.qqoq.net/{PUSH_TOKEN}.send?title={site_name}更新提醒&content=页面内容发生变动，请前往官网查看详情"
        try:
            requests.get(push_url, timeout=10)
            print(f"[{site_name}] 页面更新，已发送微信推送")
        except Exception as e:
            print(f"[{site_name}] 推送接口调用失败：{str(e)}")
        with open(record_file, "w", encoding="utf-8") as f:
            f.write(new_hash)
    else:
        print(f"[{site_name}] 页面无更新，无需推送")
