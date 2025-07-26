# 香港警方打擊白牌車新聞收集系統

這是一個自動化系統，用於收集和分析香港警方打擊非法出租車（白牌車）的新聞資訊。

## 功能特點

- 每日自動收集最新新聞
- 使用 Perplexity API 進行智能搜索
- 自動去重和數據整理
- 生成 Markdown 格式報告
- GitHub Actions 自動化部署

## 部署步驟

### 1. 創建 GitHub 儲存庫

1. 登入 GitHub，創建新儲存庫
2. 設置儲存庫為 **Public**（免費使用 GitHub Actions）
3. 上傳所有項目文件

### 2. 設置 Perplexity API Key

1. 前往 [Perplexity API](https://www.perplexity.ai/settings/api) 獲取 API Key
2. 在 GitHub 儲存庫中，點擊 **Settings** → **Secrets and variables** → **Actions**
3. 點擊 **New repository secret**
4. 名稱：`PERPLEXITY_API_KEY`
5. 值：你的 Perplexity API Key

### 3. 啟用 GitHub Actions

1. 在儲存庫中，點擊 **Actions** 標籤
2. 如果是第一次使用，點擊 **I understand my workflows, go ahead and enable them**
3. 工作流程將自動啟用

### 4. 測試運行

1. 在 **Actions** 頁面，選擇 "HK Police White Plate Car News Collector"
2. 點擊 **Run workflow** 進行手動測試
3. 檢查運行結果和生成的文件

## 自動運行時間

- **每日香港時間 0:00** 自動執行
- 對應 **UTC 16:00**
- 可以通過修改 `.github/workflows/news_collector.yml` 中的 cron 表達式調整時間

## 文件說明

- `news_collector.py`: 主要的新聞收集腳本
- `.github/workflows/news_collector.yml`: GitHub Actions 工作流程配置
- `requirements.txt`: Python 依賴包
- `hk_police_news.csv`: 收集的新聞數據（自動生成）
- `daily_report.md`: 每日報告（自動生成）

## 定制化

### 修改搜索關鍵詞
編輯 `news_collector.py` 中的 `query` 變量：
```python
query = "香港警方打擊白牌車 執法行動 拘捕"
```

### 修改執行時間
編輯 `.github/workflows/news_collector.yml` 中的 cron 表達式：
```yaml
- cron: '0 16 * * *'  # UTC 16:00 = 香港時間 0:00
```

### 添加新聞來源
編輯 `news_collector.py` 中的 `search_domain_filter`：
```python
"search_domain_filter": ["hk01.com", "mingpao.com", "scmp.com", "gov.hk", "police.gov.hk"]
```

## 注意事項

1. **API 使用限制**: Perplexity API 有使用配額限制，請合理使用
2. **儲存庫設置**: 確保儲存庫為 Public 以免費使用 GitHub Actions
3. **Secret 安全**: 不要在代碼中直接寫入 API Key
4. **時區轉換**: GitHub Actions 使用 UTC 時間，已自動轉換為香港時間

## 故障排除

### 如果工作流程失敗：
1. 檢查 API Key 是否正確設置
2. 查看 Actions 頁面的錯誤日志
3. 確認 Perplexity API 配額是否充足

### 如果沒有新數據：
1. 檢查新聞來源是否有相關報導
2. 調整搜索關鍵詞
3. 檢查日期範圍設置

## 支持

如有問題，請在 GitHub Issues 中提出。
