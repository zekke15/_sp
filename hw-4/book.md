# 📘 人話寫扣：用 AI 代理人打造專屬編譯器與虛擬機

這是一個非常棒且具有開源精神的想法！將這種「AI 驅動開發（AI-Driven Development）」與「系統程式與編譯器原理」的實戰經驗寫成一本書，發佈到 GitHub 上，絕對能幫助到無數正在網路上苦苦掙扎的資訊系學生與開發者。

為了讓你能用最快的速度把這本書生出來並上線，我已經幫你規劃好了電子書的完整大綱結構。我們可以利用 GitHub Pages 搭配現代最流行的 Markdown 電子書架構（如 MkDocs 或 VitePress），一鍵生成超漂亮的官方書籍網站！
📂 科技電子書章節大綱 (Book Outline)
前言：當系統程式碰上 2026 的大模型浪潮

為什麼傳統編譯器前端（Lexer/Parser）可以用 LLM 的低隨機性（Temperature=0.1）完美取代？

第一章：架構設計 —— 前端 LLM 與後端暫存器虛擬機

型態系統、執行模式與記憶體管理的抉擇。

四元組中間碼（Quadruples IR）的 EBNF 語法結構定義。

第二章：實戰 Aider —— 命令列 AI 代理人的極致重構

打破 Windows 環境變數魔咒：.env 本地金鑰設定檔的終極解法。

用嘴巴改扣：如何對 Aider 下達精準的重構提示詞（Prompt Engineering）。

第三章：解密虛擬機核心 —— 從算術到控制流跳轉

ADD 與 SUB 的底層變數映射（暫存器模擬）。

迴圈的魔術：利用 CMP_GT、CMP_LT 與 JMP_F 的程式計數器（PC）前向與後向跳轉。

第四章：實體化目的碼 —— .quad 檔案的誕生與二度解析

正則表達式在四元組文字流解析中的關鍵角色。

實現編譯與執行期的完全解耦。

🚀 如何在 3 分鐘內將書放上 GitHub 並產生網址？
你可以直接使用 GitHub 官方推薦的簡約單頁書籍/文件部署法。請跟著以下步驟操作：

步驟 1：在 GitHub 上建立新的儲存庫 (Repository)
登入你的 GitHub，點擊右上角的 「New」 建立新的儲存庫。

儲存庫名稱（Repository name）輸入：ai-compiler-book

設為 Public（公開），並勾選 Add a README file。

點擊 Create repository。

步驟 2：把書的內容寫進 index.html
在 GitHub 網頁上，點擊 Add file -> Create new file，將檔名命名為：

Plaintext
index.html
然後把下面這段已經寫好的美化版單頁電子書代碼整段複製並貼進去，拉到最下方點擊 Commit changes 存檔：

## 📌 前言：當系統程式碰上大模型浪潮

本專案完美體現了現代編譯器將高階抽象邏輯轉換為低階機器碼並執行的核心原理。傳統上，我們需要花費數週編寫複雜的 Lexer 與 Parser 語法樹；但在 2026 年的今天，我們可以直接利用低隨機性（Temperature=0.1）的大語言模型作為精準的前端編譯器，將人類的大白話直接翻譯成標準的四元組中間碼（Quadruples IR）。

**作者：** Ryan & Gemini AI 協同著作

**年份：** 2026年

---

## 第一章：核心架構設計 (Compiler Backend VM)

本虛擬機採用**暫存器機（Register-based VM）**架構設計。指令直接對具名的虛擬暫存器（如 total, i, t1）進行操作，而非傳統 Java Bytecode 的堆疊機模式。變數直接映射至 Python 的字典（哈希表）中，實現動態型態管理。

### EBNF 語法結構定義

quad_list      = { quadruple } ;
quadruple      = line_num ":" op "," arg1 "," arg2 "," result ;
op             = "IMM" | "ADD" | "SUB" | "STORE" | "JMP" | "JMP_F" | "CMP_LT" | "CMP_GT" ;

## 第二章：實戰 Aider —— 命令列 AI 代理人的極致重構

在 Windows 的 Git Bash 環境下，環境變數常因作業系統隔閡而失效。本書推薦的終極大絕是在專案根目錄建立 `.env` 檔案：

GEMINI_API_KEY=YOUR_API_KEY_HERE

啟動 Aider 代理人後，透過高階提示詞，AI 能在幾秒鐘內自動完成多檔案的 Git Diff 對比、代碼注入與自動 Commit 儲存。

## 第三章：解密虛擬機控制流迴圈

控制流跳轉（迴圈）是本系統的核心。以下是新加入的 `CMP_GT` 與減法指令在底層 CPU 迴圈中的運作實作：

```python
elif op == "SUB":
    self.variables[res] = self._get_val(a1) - self._get_val(a2)
elif op == "CMP_GT":
    self.variables[res] = 1 if self._get_val(a1) > self._get_val(a2) else 0
```

透過將比較結果寫入暫存器，配合 `JMP_F`（條件不成立則前向跳出）與 `JMP`（無條件後向追蹤），即可在虛擬機內部完美模擬出強大的迴圈控制流。

---

🎉 感謝閱讀！歡迎在 GitHub 上開啟 Issue 參與本書的開源修訂。
步驟 3：一鍵開啟 GitHub Pages 官方網址！
在你的 GitHub 儲存庫頁面，點擊右上角的 「Settings（設定）」（齒輪圖示）。

在左側選單找到 「Pages」 點進去。

在 Build and deployment 底下的 Branch（分支），把 None 改選為 main，後面的路徑保持 / (root)，然後點擊 「Save」。

🌐 你的專案電子書網址將會是：
等待大約 30 秒後，重新整理該頁面，GitHub 就會為你配發一個全球公開的官方書籍網址！
