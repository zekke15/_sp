import threading

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = threading.Lock()  # 建立互斥鎖 (Mutex)

    def deposit(self, amount, times):
        for _ in range(times):
            # 獲取鎖，確保臨界區操作的原子性
            with self.lock:
                self.balance += amount

    def withdraw(self, amount, times):
        for _ in range(times):
            with self.lock:
                self.balance -= amount

if __name__ == "__main__":
    account = BankAccount(balance=1000)
    times = 100000
    amount = 10
    
    print(f"初始存款金額: {account.balance}")
    print(f"同時進行存提款各自 {times} 次，每次金額: {amount}...")

    # 建立兩個執行緒，模擬同一個人同時存錢與提錢
    t1 = threading.Thread(target=account.deposit, args=(amount, times))
    t2 = threading.Thread(target=account.withdraw, args=(amount, times))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"最終存款金額: {account.balance} (預期應為: 1000)")