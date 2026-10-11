---
name: conf-papers
description: 依會議、年份與研究方向查找學術論文，比較閱讀價值並整理推薦。
---

# 會議論文搜尋

根據使用者指定的研究問題、會議與年份取得候選，說明推薦理由與資料覆蓋。搜尋、排序和深入閱讀的範圍由本次任務決定。

## 工具與設定

以本檔所在的實際目錄定位 `scripts/search_conf_papers.py`，先解析符號連結。它需要同層的 `start-my-day/scripts/search_arxiv.py` 提供共用函式，所以兩個 Skill 必須一起保留。

以 `--help` 查參數。用 `--config`、`--output` 指定檔案，依需求傳入 `--year`、`--conferences`、`--top-n`、`--max-per-venue`。目前腳本支援 CVPR、ICCV、ECCV、ICLR、AAAI、NeurIPS、ICML；其他會議可直接查官方論文集或適合的資料源。

`conf-papers.yaml` 是本 Skill 的獨立設定，含 `keywords`、`excluded_keywords`、`default_year`、`default_conferences`、`top_n`。隨附的興趣、排除詞和年份只是範例；依使用者需求選定或建立本次設定，不把預設排除 survey、3D 等規則強加給使用者。「最新」需使用目前日期和實際已公開的論文集判斷。

## 判讀候選集

腳本用 DBLP 取列表、先依標題關鍵字篩選，再用 Semantic Scholar 補摘要和引用資料。固定分數只作初篩訊號，不能視為品質結論；已被過濾的論文不會出現在結果中。

若術語不一致、結果過少、漏掉重要工作或任務需要廣泛覆蓋，可調整查詢和排除詞、增大候選集，或補查會議官網、OpenReview、作者頁面及引用。明確區分資料源失敗、論文集尚未收錄和真正零結果。

根據問題契合度、方法與實驗證據安排推薦順序，不固定只分析前三篇。深入分析需要時讀同層 `paper-analyze/SKILL.md`；沒有 arXiv ID 的論文可使用出版者或本地 PDF。

## 交付

提供標題、會議與年份、來源連結、推薦理由及關鍵限制。摘要初讀與全文分析需區分。篇數、章節和圖片按需求決定。

需要存檔時使用指定 Vault、`OBSIDIAN_VAULT_PATH` 或已選設定的 `vault_path`，沿用既有目錄（預設每日推薦在 `10_Daily/`）。位置未定可先在對話回覆；寫入前取得位置。按 ID、DOI 或標題查重，保留人工筆記。語言依使用者要求，其次設定，最後跟隨對話。Obsidian 連結使用 `[[路徑|名稱]]`。
