import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, philosopher_id, left_chopstick, right_chopstick):
        super().__init__()
        self.philosopher_id = philosopher_id
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self):
        for i in range(2):  # 每個哲學家輪流吃 2 次飯
            self.think()
            self.eat(i + 1)

    def think(self):
        print(f"🤔 [思考] 哲學家 {self.philosopher_id} 開始沉思...")
        time.sleep(random.uniform(0.1, 0.3))

    def eat(self, round_num):
        # 💡 核心同步策略：打破「循環等待」
        # 奇數號哲學家先左後右；偶數號哲學家先右後左
        if self.philosopher_id % 2 == 1:
            first_chopstick = self.left_chopstick
            second_chopstick = self.right_chopstick
            first_dir, second_dir = "左", "右"
        else:
            first_chopstick = self.right_chopstick
            second_chopstick = self.left_chopstick
            first_dir, second_dir = "右", "左"

        print(f"👀 [飢餓] 哲學家 {self.philosopher_id} 肚子餓了，企圖去拿 {first_dir}手邊 筷子")
        
        # 嘗試獲取第一隻筷子
        first_chopstick.acquire()
        print(f"🥢 [取得] 哲學家 {self.philosopher_id} 成功拿起了 {first_dir}手邊 筷子")
        
        # 刻意微小延遲，若演算法有死鎖漏洞，此處最容易觸發集體卡死
        time.sleep(0.05) 
        
        print(f"🔍 [尋找] 哲學家 {self.philosopher_id} 試圖索取 {second_dir}手邊 筷子...")
        # 嘗試獲取第二隻筷子
        second_chopstick.acquire()
        print(f"🍱 [享用] 哲學家 {self.philosopher_id} 集齊兩隻筷子！開始吃第 {round_num} 頓飯")
        time.sleep(random.uniform(0.1, 0.2))
        
        # 用餐完畢，釋放資源
        second_chopstick.release()
        first_chopstick.release()
        print(f"🏳️ [放回] 哲學家 {self.philosopher_id} 吃飽了，放下了兩隻筷子。")

if __name__ == "__main__":
    num_philosophers = 5
    print("=== 🚀 哲學家就座，並行監控系統啟動 ===")
    
    # 建立 5 隻筷子（5 把獨立的互斥鎖）
    chopsticks = [threading.Lock() for _ in range(num_philosophers)]
    
    # 初始化並啟動哲學家執行緒
    philosophers = []
    for i in range(num_philosophers):
        left = chopsticks[i]
        right = chopsticks[(i + 1) % num_philosophers]
        
        p = Philosopher(i, left, right)
        philosophers.append(p)
        p.start()

    # 等待所有執行緒執行完畢
    for p in philosophers:
        p.join()
        
    print("\n=== ✅ 所有哲學家都順利吃飽，系統成功規避死鎖與活鎖 ===")