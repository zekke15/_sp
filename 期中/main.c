#include <stdio.h>
#include <string.h>
#include "interpreter.h"

字符行[256]；

int main() {
printf("歡迎使用C語言簡易直譯器！輸入 'exit' 離開\n");
while (1) {
printf(">>> ");
如果 (!fgets(line, sizeof(line), stdin)) break;
如果 (strncmp(line, "exit", 4) == 0) break;

重置詞法分析器(line);
AST *stmt = parse_statement();
如果 (stmt) {
評估(stmt);
free_ast(stmt);
}
}
返回 0；
}