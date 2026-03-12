# QuietMind MVP (Python / Streamlit)

一個 mobile-first、低刺激、可快速完成第一次體驗的心理狀態整理 Web App。

## 已完成的 MVP 功能

### 公開區
- 首頁
- 這個服務適合你嗎
- 隱私與安全
- 心理資源 / 轉介
- 危機支援
- 登入 / 註冊

### 登入後
- Onboarding 6 步驟
  - 使用目標
  - WHO-5
  - BSRS-5
  - 六維度盤點
  - 偏好設定
  - 檢查答案
- 今日首頁 Dashboard
- 30 秒校準
- 決策前檢查
- 每週回顧
- 報告中心
- 工具箱
- 我的設定
- 資料匯出 / 刪除
- 快速離開

## 本機執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 最快上架：Streamlit Community Cloud

1. 建立 GitHub repo
2. 把 `app.py`、`requirements.txt`、`README.md` 推上去
3. 到 Streamlit Community Cloud 登入
4. 選你的 repo 與 `app.py`
5. 點 Deploy

## 第二快上架：Render / Railway

如果你之後要：
- 自訂網域
- 更穩定的後端服務
- 接 PostgreSQL
- 做 staging / production

可以改上 Render 或 Railway。

## 後續建議

第一版先保持現在的閉環：
- 第一次進站 → 適合度檢查 → 註冊 → Onboarding → Dashboard
- 日常使用 → 30 秒校準 / 決策前檢查
- 每週 → 每週回顧 / 報告中心
- 危機 → 危機支援 / 一般資源

再下一版再補：
- 真正的 Email 驗證
- PostgreSQL
- 管理後台
- 地區化資源資料庫
- PDF 週報
- 更完整的 consent log
