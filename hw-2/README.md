# 虛擬機內部透過一個 while pc < total_instructions

的無窮迴圈來模擬 CPU 的時脈。以下是核心指令的底層實作邏輯：

以下是核心指令的底層實作邏輯：1. 資料傳輸與賦值指令IMM, val, -, res：立即數載入。虛擬機將字串 val 轉為整數後，直接寫入暫存器 res。Pythonif op == "IMM":

    self.variables[res] = int(a1)
STORE, arg1, -, res：暫存器複製（類似組合語言的 MOV）。將 arg1 的數值複製到 res 中。2. 算術與邏輯運算指令ADD, arg1, arg2, res：加法運算。動態讀取 arg1 與 arg2 的數值（如果是常數則直接解析，若是變數則從環境中查找），相加後寫入 res。CMP_LT, arg1, arg2, res：小於比較。若 arg1 < arg2，則將布林值 1 寫入 res，否則寫入 0。3. 控制流跳轉指令（迴圈的核心）這是實作 while 迴圈最重要的兩條指令：JMP_F, cond, -, target_line：條件跳轉。檢查 cond 暫存器的值。如果為 0（代表條件不成立、迴圈該結束了），則強制將程式計數器 pc 修改為 target_line，實現前向跳出迴圈。Pythonelif op == "JMP_F":
    if self._get_val(a1) == 0:
        pc = int(res)
        continue  # 跳過底部的 pc += 1，直接進入目標行執行
JMP, -, -, target_line：無條件跳轉。當程式執行到迴圈體的最底部時，必須無條件將 pc 修改回迴圈開頭的條件判斷處 (target_line)，實現後向無窮迴圈追蹤。
🧪 程式追蹤與執行生命週期以作業中的經典 Prompt 為例："幫我做一個迴圈，計算 1 加到 10 的總和，結果存到 total 變數中"1. 編譯期 (AI Front-end Output)AI 接收到 Prompt 後，會精準生成以下中間碼。注意其中 003 的 JMP_F 與 006 的 JMP 完美的形成了闭环控制流：Plaintext000: IMM, 0, -, total    # 初始化 total = 0
001: IMM, 1, -, i        # 初始化 計數器 i = 1
002: CMP_LT, i, 11, t1   # 檢查 i < 11 (即 i 1到10)
003: JMP_F, t1, -, 007   # 如果 t1 為 0 (i=11)，跳出迴圈到 007 行
004: ADD, total, i, total# total = total + i
005: ADD, i, 1, i        # i = i + 1
006: JMP, -, -, 002      # 無條件跳回 002 行重新檢查條件
007: ... (結束)
2. 執行期 (VM Runtime Execution Trace)第 1 次迭代：i=1, total=0 $\rightarrow$ i<11 成立 ($t1=1$) $\rightarrow$ 不跳轉 $\rightarrow$ total=1, i=2 $\rightarrow$ 跳回行 002。第 10 次迭代：i=10, total=45 $\rightarrow$ i<11 成立 ($t1=1$) $\rightarrow$ 不跳轉 $\rightarrow$ total=55, i=11 $\rightarrow$ 跳回行 002。第 11 次檢查：i=11, total=55 $\rightarrow$ i<11 不成立 ($t1=0$) $\rightarrow$ 觸發 JMP_F 跳轉至行 007 $\rightarrow$ 迴圈安全退出。
⚠️ 常見運行錯誤：503 UNAVAILABLE 處理機制在執行過程中，若遇到 503 UNAVAILABLE 錯誤，這屬於非程式碼性錯誤。原因分析：由於專案使用的是 Google AI Studio 的免費共用速率限制 (Rate Limits)，當全球多個客戶端在同一秒內發送過多 gemini-2.5-flash 請求時，Google 伺服器會拋出流量尖峰保護機制。架構優化對策：重試機制 (Backoff Retry)：直接重新執行命令 python ai_compiler.py，通常 2-3 次內即可成功配對到伺服器資源。模型級別退避 (Model Fallback)：將 model='gemini-2.5-flash' 改為 model='gemini-2.5-pro' 或 model='gemini-1.5-flash'，分流至不同負載的伺服器叢集。
