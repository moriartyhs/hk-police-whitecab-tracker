
import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import csv

class HKPoliceNewsCollector:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search_news(self, query, start_date, end_date):
        """Search for news using Perplexity API"""
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一個專業的新聞收集助手，專門收集香港警方打擊白牌車的新聞資訊。請提供準確的日期、標題、內容摘要和新聞來源。"
                },
                {
                    "role": "user", 
                    "content": f"請搜索並整理{start_date}至{end_date}期間的{query}相關新聞，請包含：日期、標題、內容摘要、執法行動詳情、影響、新聞來源。請以JSON格式返回結果。"
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
            "top_p": 0.9,
            "return_citations": True,
            "search_domain_filter": ["hk01.com", "mingpao.com", "scmp.com", "gov.hk", "police.gov.hk"]
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API請求錯誤: {e}")
            return None

    def parse_news_response(self, response):
        """解析API響應並提取新聞數據"""
        if not response or 'choices' not in response:
            return []

        content = response['choices'][0]['message']['content']

        # 嘗試解析JSON內容
        try:
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                news_data = json.loads(json_match.group())
                return news_data
        except:
            pass

        # 如果無法解析JSON，使用正則表達式提取信息
        news_items = []
        lines = content.split('\n')
        current_item = {}

        for line in lines:
            line = line.strip()
            if '日期:' in line or '時間:' in line:
                current_item['date'] = line.split(':', 1)[1].strip()
            elif '標題:' in line:
                current_item['title'] = line.split(':', 1)[1].strip()
            elif '摘要:' in line or '內容:' in line:
                current_item['description'] = line.split(':', 1)[1].strip()
            elif '行動:' in line or '執法:' in line:
                current_item['action'] = line.split(':', 1)[1].strip()
            elif '影響:' in line or '結果:' in line:
                current_item['impact'] = line.split(':', 1)[1].strip()
            elif '來源:' in line:
                current_item['source'] = line.split(':', 1)[1].strip()
                if current_item.get('date') and current_item.get('title'):
                    news_items.append(current_item.copy())
                current_item = {}

        return news_items

    def save_to_csv(self, news_data, filename='hk_police_news.csv'):
        """將新聞數據保存到CSV文件"""
        if not news_data:
            print("沒有新聞數據需要保存")
            return

        fieldnames = ['date', 'title', 'description', 'action', 'impact', 'source']

        # 檢查文件是否存在，如果存在則讀取現有數據
        existing_data = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                existing_data = list(reader)

        # 合併數據並去重
        all_data = existing_data + news_data
        unique_data = []
        seen_titles = set()

        for item in all_data:
            title = item.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_data.append(item)

        # 按日期排序
        unique_data.sort(key=lambda x: x.get('date', ''), reverse=True)

        # 保存到CSV
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_data)

        print(f"已保存 {len(unique_data)} 條新聞記錄到 {filename}")

    def generate_markdown_report(self, csv_filename='hk_police_news.csv'):
        """生成Markdown格式報告"""
        if not os.path.exists(csv_filename):
            return "沒有找到新聞數據文件"

        df = pd.read_csv(csv_filename, encoding='utf-8')

        if df.empty:
            return "沒有新聞數據"

        # 生成統計信息
        total_news = len(df)
        latest_date = df['date'].iloc[0] if not df.empty else "無"

        # 生成報告
        report = f"""# 2025年香港警方打擊白牌車執法行動數據分析報告

## 數據摘要
- 總計新聞數量：{total_news}
- 最新更新日期：{latest_date}
- 報告生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 執法行動詳細記錄

| 日期 | 標題 | 摘要 | 行動詳情 | 影響 | 來源 |
|------|------|------|----------|------|------|
"""

        for _, row in df.iterrows():
            report += f"| {row.get('date', '')} | {row.get('title', '')} | {row.get('description', '')} | {row.get('action', '')} | {row.get('impact', '')} | {row.get('source', '')} |\n"

        report += f"""
## 更新說明
此報告由自動化系統於香港時間每日0點更新，數據來源包括香港主要新聞媒體。

---
*最後更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} HKT*
"""

        return report

    def collect_daily_news(self):
        """每日新聞收集主函數"""
        # 搜索前一天的新聞
        yesterday = datetime.now() - timedelta(days=1)
        start_date = yesterday.strftime('%Y-%m-%d')
        end_date = yesterday.strftime('%Y-%m-%d')

        query = "香港警方打擊白牌車 執法行動 拘捕"

        print(f"開始收集 {start_date} 的新聞...")

        # 調用API搜索新聞
        response = self.search_news(query, start_date, end_date)

        if response:
            news_data = self.parse_news_response(response)
            if news_data:
                self.save_to_csv(news_data)
                report = self.generate_markdown_report()

                # 保存報告
                with open('daily_report.md', 'w', encoding='utf-8') as f:
                    f.write(report)

                print("新聞收集和報告生成完成！")
            else:
                print("未找到相關新聞")
        else:
            print("API調用失敗")

if __name__ == "__main__":
    collector = HKPoliceNewsCollector()
    collector.collect_daily_news()
