#include <ctype.h>
#include <string.h>
#include "interpreter.h"

static const char *src;
靜態令牌電流；

void reset_lexer(const char *input) {
src = 輸入；
}

Token get_next_token() {
while (isspace(*src)) src++;

如果 (*src == '\0') 返回 (Token){TOKEN_EOF, ""};
如果 (isdigit(*src)) {
int i = 0;
while (isdigit(*src)) current.text[i++] = *src++;
current.text[i] = '\0';
current.type = TOKEN_NUMBER;
返回電流；
}
如果 (isalpha(*src)) {
int i = 0;
while (isalnum(*src)) current.text[i++] = *src++;
current.text[i] = '\0';
如果 (strcmp(current.text, "print") == 0)
current.type = TOKEN_PRINT;
別的
current.type = TOKEN_IDENTIFIER;
返回電流；
}
如果 (*src == '=') {
src++;
返回 (Token){TOKEN_ASSIGN, "="};
}
如果 (strchr("+-*/()", *src)) {
current.type = TOKEN_OPERATOR;
current.text[0] = *src++;
current.text[1] = '\0';
返回電流；
}

src++; // 跳過未知
返回 (Token){TOKEN_EOF, ""};
}
