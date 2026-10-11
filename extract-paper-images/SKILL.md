---
name: extract-paper-images
description: 從 arXiv 論文來源或本地 PDF 提取原圖，供閱讀、分析或筆記引用。
---

# 提取論文原圖

依使用者要求取得全部圖片或特定圖表，保留來源及可辨識的檔名。輸入可以是 arXiv ID、URL 或本地 PDF；呼叫腳本前把 URL／`arXiv:` 前綴整理成純 ID。

## 腳本介面

`scripts/extract_images.py` 相對於本檔的實際目錄；解析符號連結後使用絕對路徑，以已安裝 PyMuPDF 和 requests 的 Python 執行：

```text
python <skill-directory>/scripts/extract_images.py <arxiv-id-or-local-pdf> <output-directory> <index-file>
```

目的地以使用者指定位置或既有論文筆記的 `images/` 為準；僅作臨時分析時使用本次工作的暫存目錄。腳本會寫出圖片與索引，先檢查重名避免覆蓋既有素材。

## 選擇提取方式

腳本優先取 arXiv 源碼中的圖片和獨立 figure PDF，再利用本地 PDF 提取嵌入圖片。若只傳 ID 且來源失敗，它不會自動下載整篇 PDF 作備援：需自行下載 PDF，再傳入本地檔案路徑。

純向量圖／TikZ 可能沒有嵌入圖片；此時檢查 PDF 頁面與圖說位置，裁切相應區域，保留座標軸、圖例等必要內容。使用當前環境的 PDF／圖片工具，不要求特定代理的工具名稱。

檢視提取結果，確認圖片清晰、內容完整，並以圖說或頁碼判定用途；檔案排序不代表論文圖號。按任務排除 logo 和裝飾圖，不以固定數量決定是否提取成功。缺失時說明原因，不生成替代內容冒充原圖。

回傳實際檔案位置、來源／圖號（可確認時）及索引。寫入 Obsidian 時以含路徑的 `![[路徑/圖片.png|600]]` 嵌入；聊天回覆使用客戶端可開啟的路徑。
