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
        for _ in range(3): # 每個哲學家吃 3 次飯
            self.think()
            self.eat()

    def think(self):
        print(f"🤔 哲學家 {self.philosopher_id} 正在思考...")
        time.sleep(random.uniform(0.1, 0.3))

    def eat(self):
        # 💡 死鎖預防策略：打破「循環等待」條件
        # 規定：奇數號哲學家先拿左邊，偶數號哲學家先拿右邊
        if self.philosopher_id % 2 == 1:
            first_chopstick = self.left_chopstick
            second_chopstick = self.right_chopstick
        else:
            first_chopstick = self.right_chopstick
            second_chopstick = self.left_chopstick

        # 開始拿第一隻筷子
        first_chopstick.acquire()
        print(f"🥢 哲學家 {self.philosopher_id} 拿起了第一隻筷子")
        
        # 稍微耽擱一下，如果會死鎖，此處最容易觸發
        time.sleep(0.1) 
        
        # 開始拿第二隻筷子
        second_chopstick.acquire()
        print(f"🍱 哲學家 {self.philosopher_id} 成功拿到兩隻筷子，開始大口吃飯！")
        time.sleep(random.uniform(0.1, 0.3))
        
        # 吃完放下筷子
        second_chopstick.release()
        first_chopstick.release()
        print(f"🏳️ 哲學家 {self.philosopher_id} 吃飽了，放下了兩隻筷子")

if __name__ == "__main__":
    num_philosophers = 5
    # 建立 5 隻筷子（5 把互斥鎖）
    chopsticks = [threading.Lock() for _ in range(num_philosophers)]
    
    philosophers = []
    for i in range(num_philosophers):
        # 每個哲學家左右兩邊的筷子編號
        left = chopsticks[i]
        right = chopsticks[(i + 1) % num_philosophers]
        
        p = Philosopher(i, left, right)
        philosophers.append(p)
        p.start()

    for p in philosophers:
        p.join()
        
    print("=== 所有哲學家都順利吃飽，沒有人餓死（無死鎖） ===")
    