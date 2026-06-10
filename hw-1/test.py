// 測試：計算 1 加到 5 的總和 (利用 while 迴圈)
// 同時測試函數呼叫機制與引數傳遞

func add(x, y) {
    return x + y;
}

sum = 0;
i = 1;

while (i < 6) {
    sum = add(sum, i); // 呼叫 add 函數
    i = i + 1;
}

// 執行完畢後，全域變數 sum 應該要等於 15