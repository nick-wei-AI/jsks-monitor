name: Page Monitor
on:
  schedule:
    # 定时规则：UTC时间，北京时间=UTC+8；下面 cron 每30分钟执行一次
    - cron: "*/30 * * * *"
  workflow_dispatch: # 支持手动点按钮立即运行测试

jobs:
  monitor_job:
    runs-on: ubuntu-latest
    steps:
      - name: 拉取仓库代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: 配置Python环境
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: 执行监控脚本
        env:
          PUSH_TOKEN: ${{ secrets.PUSH_TOKEN }}
          TARGET_URL: ${{ secrets.TARGET_URL }}
        run: python3 monitor.py

      - name: 提交更新后的哈希记录
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "actions@github.com"
          git add hash_record.txt
          git diff --quiet && git diff --staged --quiet || (git commit -m "auto update hash" && git push)
