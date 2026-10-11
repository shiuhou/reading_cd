---
name: start-my-day
description: 依研究興趣尋找近期論文、比較閱讀價值，整理每日推薦與 Obsidian 筆記。
---

# 每日論文推薦

目標是幫使用者決定值得讀什麼，以及為什麼。依問題選擇搜尋範圍、來源、篇數及分析深度；使用者指定的條件優先於範例和腳本預設。

## 環境與輸出

- 將本檔所在的實際目錄作為 `SKILL_DIR`，解析符號連結後定位腳本；它不是系統預設環境變數。使用已安裝依賴的 Python 環境和當前代理可用的工具。
- 研究設定優先採用使用者指定檔案，其次是 `RESEARCH_CONFIG_PATH`，再其次是 `$OBSIDIAN_VAULT_PATH/99_System/Config/research_interests.yaml`。倉庫的 `config.example.yaml` 只是範例興趣，不能視為使用者偏好。
- Vault 路徑取使用者指定值、`OBSIDIAN_VAULT_PATH` 或已選設定的 `vault_path`。未指定儲存位置時可先在對話回覆；寫入前取得具體位置。語言依使用者要求，其次設定，最後跟隨對話。
- 沿用現有筆記結構；預設論文目錄 `20_Research/Papers/`、每日筆記 `10_Daily/`。檔名日期以使用者時區或指定日期為準。暫存 JSON 放本次工作的獨立目錄。

## 搜尋與判斷

可用 `scripts/search_arxiv.py` 取得候選論文；先以 `--help` 查參數。傳入明確的 `--config`、`--output`、`--target-date`，依需求調整 `--focus`、`--days`、`--categories`、`--max-results` 和 `--top-n`。

這支腳本會以關鍵字過濾及啟發式分數排序，也會裁切候選數量。分数是初篩訊號，並非科學品質的測量。需要較廣覆蓋時擴大候選集，或直接補查 arXiv、Semantic Scholar、出版者、會議官方網站和相關引用；不要把腳本返回的清單當作完整文獻集合。API 失敗與真正沒有結果要分別說明。

根據研究問題、方法與證據選擇閱讀順序。可以調整排序、補入低引用但相關的工作、比較互相矛盾的結果。說明實際搜尋範圍與選擇理由；僅讀摘要時明確標示，不能據此宣稱已驗證實驗或原創性。

詳細分析與圖片提取依本次目標安排，不固定前三篇，也不要求每篇都有圖片。需要時讀取同層 `paper-analyze/SKILL.md` 或 `extract-paper-images/SKILL.md`，按其中的工具說明執行；Skill 名稱不是 shell 指令。

## 筆記

寫入前按 ID、DOI 或標題查重，保留既有人工筆記。提供論文連結、閱讀理由、重要結果的出處及未解問題，結構依本次用途決定。Obsidian 連結使用 `[[路徑|顯示名稱]]`，圖片使用含路徑的 `![[路徑/圖片.png|600]]`，避免重名。

大型 Vault 可用 `scripts/scan_existing_notes.py --vault ... --papers-dir ... --output ...` 建索引；只需找少數論文時直接搜尋即可。`scripts/link_keywords.py` 可選用，輸出到暫存副本後檢查連結，再更新目標筆記。只連到實際存在的筆記。
