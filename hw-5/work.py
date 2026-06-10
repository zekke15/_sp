import threading
import time
import random
from queue import Queue

class BufferQueue:
    def __init__(self, max_size=5):
        self.queue = []
        self.max_size = max_size
        self.condition = threading.Condition() # 使用條件變數進行同步

    def produce(self, item):
        with self.condition:
            # 如果緩衝區滿了，生產者必須等待
            while len(self.queue) == self.max_size:
                print("⚠️ 緩衝區滿了！生產者暫停等待...")
                self.condition.wait()
            
            self.queue.append(item)
            print(f"📦 [生產者] 生產了: {item} | 緩衝區數量: {len(self.queue)}")
            
            # 通知正在等待的消費者
            self.condition.notify_all()

    def consume(self):
        with self.condition:
            # 如果緩衝區空了，消費者必須等待
            while len(self.queue) == 0:
                print("⚠️ 緩衝區空了！消費者暫停等待...")
                self.condition.wait()
            
            item = self.queue.pop(0)
            print(f"😋 [消費者] 消費了: {item} | 緩衝區數量: {len(self.queue)}")
            
            # 通知正在等待的生產者
            self.condition.notify_all()
            return item

def producer_worker(buffer, count):
    for i in range(count):
        buffer.produce(f"產品-{i+1}")
        time.sleep(random.uniform(0.1, 0.3))

def consumer_worker(buffer, count):
    for _ in range(count):
        buffer.consume()
        time.sleep(random.uniform(0.2, 0.5))

if __name__ == "__main__":
    shared_buffer = BufferQueue(max_size=5)
    
    # 建立生產者與消費者執行緒
    p = threading.Thread(target=producer_worker, args=(shared_buffer, 10))
    c = threading.Thread(target=consumer_worker, args=(shared_buffer, 10))
    
    p.start()
    c.start()
    
    p.join()
    c.join()
    print("=== 生產與消費管線結束 ===")