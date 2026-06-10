import os
import re
from google import genai
from google.genai import types

# =========================================================
# 1. AI 前端設定 (自然語言 -> 中間碼)
# =========================================================
def ask_ai_to_compile(user_prompt: str) -> str:
    """
    利用 Gemini AI 將使用者的自然語言，編譯成標準的四元組中間碼。
    """
    # 這裡已經幫你把剛才複製的 API Key 直接寫進 Client 初始化中
    client = genai.Client(api_key="AQ.Ab8RN6J51i34nXaJAYEORDO5MKP9UqwM4k9OA0s6XKJpHaZ5Ew")
    
    # 給予 AI 系統指令（System Instruction），強迫它當一個編譯器前端
    system_instruction = """
    你是一個嚴格的中間碼編譯器前端。你的任務是將使用者的自然語言，翻譯成四元組中間碼。
    你只能輸出中間碼，絕對不能包含任何標題、Markdown 語法（不要用 ```）、或任何解釋。
    
    支援的操作碼 (Opcode):
    - IMM, val, -, res (將常數 val 存入 res)
    - ADD, arg1, arg2, res (res = arg1 + arg2)
    - SUB, arg1, arg2, res (res = arg1 - arg2)
    - STORE, arg1, -, res (res = arg1)
    - CMP_LT, arg1, arg2, res (若 arg1 < arg2 則 res=1 否則 0)
    - CMP_GT, arg1, arg2, res (若 arg1 > arg2 則 res=1 否則 0)
    - JMP_F, cond, -, target_line (若 cond 為 0 則跳到 target_line)
    - JMP, -, -, target_line (無條件跳到 target_line)
    
    輸出格式範例（嚴格遵照此格式，每行一個）：
    000: IMM, 0, -, sum
    001: IMM, 1, -, i
    002: CMP_LT, i, 6, t1
    003: JMP_F, t1, -, 007
    004: ADD, sum, i, sum
    005: ADD, i, 1, i
    006: JMP, -, -, 002
    """

    print("🤖 AI 編譯中...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1, # 低隨機性，確保生成的程式碼結構穩定
        )
    )
    return response.text.strip()

# =========================================================
# 2. 虛擬機後端 (解譯執行四元組)
# =========================================================
class VirtualMachine:
    def __init__(self):
        self.variables = {}
        self.quads = []

    def load_quads(self, quad_text: str):
        """
        將 AI 生成的文字解析成虛擬機可讀的結構
        """
        self.quads = []
        lines = quad_text.strip().split('\n')
        for line in lines:
            if not line: continue
            # 解析 000: OP, arg1, arg2, res
            match = re.match(r"(\d+):\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,\n]+)", line)
            if match:
                _, op, arg1, arg2, res = [m.strip() for m in match.groups()]
                self.quads.append({"op": op, "arg1": arg1, "arg2": arg2, "result": res})

    def _get_val(self, name: str) -> int:
        if name.isdigit() or (name.startswith('-') and name[1:].isdigit()):
            return int(name)
        return self.variables.get(name, 0)

    def run(self):
        """
        執行中間碼的模擬迴圈 (Program Counter 控制)
        """
        pc = 0
        total_instructions = len(self.quads)
        print("\n=== ⚙️ 虛擬機開始執行 ===")
        
        while pc < total_instructions:
            q = self.quads[pc]
            op, a1, a2, res = q["op"], q["arg1"], q["arg2"], q["result"]
            
            if op == "IMM":
                self.variables[res] = int(a1)
            elif op == "ADD":
                self.variables[res] = self._get_val(a1) + self._get_val(a2)
            elif op == "SUB": # 新增 SUB 操作碼
                self.variables[res] = self._get_val(a1) - self._get_val(a2)
            elif op == "STORE":
                self.variables[res] = self._get_val(a1)
            elif op == "CMP_LT":
                self.variables[res] = 1 if self._get_val(a1) < self._get_val(a2) else 0
            elif op == "CMP_GT": # 新增 CMP_GT 操作碼
                self.variables[res] = 1 if self._get_val(a1) > self._get_val(a2) else 0
            elif op == "JMP_F":
                if self._get_val(a1) == 0:
                    pc = int(res)
                    continue
            elif op == "JMP":
                pc = int(res)
                continue
            
            pc += 1
            
        print("=== ✅ 執行完畢 ===\n")
        print("最後變數狀態:")
        for k, v in self.variables.items():
            if not k.startswith('t'): # 隱藏過渡用的暫存變數 (如 t1, t2)
                print(f">> {k} = {v}")

# =========================================================
# 3. 主程式
# =========================================================
if __name__ == "__main__":
    # 測試 Prompt：你可以自由修改這句大白話，測試 AI 的編譯能力！
    prompt = "幫我做一個迴圈，計算 1 加到 10 的總和，結果存到 total 變數中"
    
    print(f"使用者輸入: '{prompt}'\n")
    
    try:
        # 1. 讓 AI 生成中間碼
        compiled_code = ask_ai_to_compile(prompt)
        print("\n[AI 編譯產出的中間碼]:")
        print("--------------------------------------------")
        print(compiled_code)
        print("--------------------------------------------")

        # 3. 將中間碼寫入 output.quad 檔案
        output_filename = "output.quad"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(compiled_code)
        print(f"中間碼已儲存至檔案: {output_filename}\n")
        
        # 2. 送進虛擬機執行
        vm = VirtualMachine()
        vm.load_quads(compiled_code)
        vm.run()
        
    except Exception as e:
        print(f"發生錯誤: {e}")
