# C 語言簡易直譯器專案 - 六大檔案說明

## 專案檔案列表

| 檔案名稱         | 功能描述                     |
|------------------|------------------------------|
| `main.c`         | 主函式與 REPL 介面            |
| `lexer.c`        | 將字串分割成 Token            |
| `parser.c`       | 將 Token 建立成 AST           |
| `eval.c`         | AST 的運算與執行邏輯          |
| `symbol_table.c` | 儲存與查詢變數的 Symbol Table |
| `interpreter.h`  | 公用結構定義與函式宣告        |

---

## 🔸 main.c

```c
#include <stdio.h>
#include <string.h>
#include "interpreter.h"

char line[256];

int main() {
    printf("歡迎使用 C 語言簡易直譯器！輸入 'exit' 離開\n");
    while (1) {
        printf(">>> ");
        if (!fgets(line, sizeof(line), stdin)) break;
        if (strncmp(line, "exit", 4) == 0) break;

        reset_lexer(line);
        AST *stmt = parse_statement();
        if (stmt) {
            eval(stmt);
            free_ast(stmt);
        }
    }
    return 0;
}
```

---

## 🔸 lexer.c

```c
#include <ctype.h>
#include <string.h>
#include "interpreter.h"

static const char *src;
static Token current;

void reset_lexer(const char *input) {
    src = input;
}

Token get_next_token() {
    while (isspace(*src)) src++;

    if (*src == '\0') return (Token){TOKEN_EOF, ""};
    if (isdigit(*src)) {
        int i = 0;
        while (isdigit(*src)) current.text[i++] = *src++;
        current.text[i] = '\0';
        current.type = TOKEN_NUMBER;
        return current;
    }
    if (isalpha(*src)) {
        int i = 0;
        while (isalnum(*src)) current.text[i++] = *src++;
        current.text[i] = '\0';
        if (strcmp(current.text, "print") == 0)
            current.type = TOKEN_PRINT;
        else
            current.type = TOKEN_IDENTIFIER;
        return current;
    }
    if (*src == '=') {
        src++;
        return (Token){TOKEN_ASSIGN, "="};
    }
    if (strchr("+-*/()", *src)) {
        current.type = TOKEN_OPERATOR;
        current.text[0] = *src++;
        current.text[1] = '\0';
        return current;
    }

    src++; // skip unknown
    return (Token){TOKEN_EOF, ""};
}
```

---

## 🔸 parser.c

```c
#include <stdlib.h>
#include <string.h>
#include "interpreter.h"

static Token lookahead;

static void advance() {
    lookahead = get_next_token();
}

static AST *parse_expr();

static AST *parse_primary() {
    if (lookahead.type == TOKEN_NUMBER) {
        AST *node = malloc(sizeof(AST));
        node->kind = AST_NUM;
        node->value = atoi(lookahead.text);
        advance();
        return node;
    } else if (lookahead.type == TOKEN_IDENTIFIER) {
        AST *node = malloc(sizeof(AST));
        node->kind = AST_VAR;
        strcpy(node->name, lookahead.text);
        advance();
        return node;
    }
    return NULL;
}

static AST *parse_term() {
    AST *node = parse_primary();
    while (lookahead.type == TOKEN_OPERATOR &&
           (lookahead.text[0] == '*' || lookahead.text[0] == '/')) {
        char op = lookahead.text[0];
        advance();
        AST *right = parse_primary();
        AST *newnode = malloc(sizeof(AST));
        newnode->kind = AST_BINOP;
        newnode->op = op;
        newnode->left = node;
        newnode->right = right;
        node = newnode;
    }
    return node;
}

static AST *parse_expr() {
    AST *node = parse_term();
    while (lookahead.type == TOKEN_OPERATOR &&
           (lookahead.text[0] == '+' || lookahead.text[0] == '-')) {
        char op = lookahead.text[0];
        advance();
        AST *right = parse_term();
        AST *newnode = malloc(sizeof(AST));
        newnode->kind = AST_BINOP;
        newnode->op = op;
        newnode->left = node;
        newnode->right = right;
        node = newnode;
    }
    return node;
}

AST *parse_statement() {
    advance();
    if (lookahead.type == TOKEN_IDENTIFIER) {
        Token var = lookahead;
        advance();
        if (lookahead.type == TOKEN_ASSIGN) {
            advance();
            AST *rhs = parse_expr();
            AST *node = malloc(sizeof(AST));
            node->kind = AST_ASSIGN;
            strcpy(node->name, var.text);
            node->expr = rhs;
            return node;
        }
    }
    if (lookahead.type == TOKEN_PRINT) {
        advance();
        AST *expr = parse_expr();
        AST *node = malloc(sizeof(AST));
        node->kind = AST_PRINT;
        node->expr = expr;
        return node;
    }
    return NULL;
}

void free_ast(AST *node) {
    if (!node) return;
    if (node->kind == AST_BINOP) {
        free_ast(node->left);
        free_ast(node->right);
    } else if (node->kind == AST_ASSIGN || node->kind == AST_PRINT) {
        free_ast(node->expr);
    }
    free(node);
}
```

---

## 🔸 eval.c

```c
#include <stdio.h>
#include "interpreter.h"

int eval(AST *node) {
    if (!node) return 0;
    switch (node->kind) {
        case AST_NUM:
            return node->value;
        case AST_VAR:
            return get_variable(node->name);
        case AST_BINOP: {
            int l = eval(node->left);
            int r = eval(node->right);
            switch (node->op) {
                case '+': return l + r;
                case '-': return l - r;
                case '*': return l * r;
                case '/': return r ? l / r : 0;
            }
        }
        case AST_ASSIGN: {
            int val = eval(node->expr);
            set_variable(node->name, val);
            return val;
        }
        case AST_PRINT: {
            int val = eval(node->expr);
            printf("%d\n", val);
            return val;
        }
    }
    return 0;
}
```

---

## 🔸 symbol_table.c

```c
#include <string.h>
#include <stdlib.h>

typedef struct {
    char name[64];
    int value;
} Var;

static Var vars[100];
static int var_count = 0;

void set_variable(const char *name, int value) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(vars[i].name, name) == 0) {
            vars[i].value = value;
            return;
        }
    }
    strcpy(vars[var_count].name, name);
    vars[var_count].value = value;
    var_count++;
}

int get_variable(const char *name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(vars[i].name, name) == 0) {
            return vars[i].value;
        }
    }
    return 0;
}
```

---

## 🔸 interpreter.h

```c
#ifndef INTERPRETER_H
#define INTERPRETER_H

typedef enum {
    TOKEN_NUMBER,
    TOKEN_IDENTIFIER,
    TOKEN_OPERATOR,
    TOKEN_ASSIGN,
    TOKEN_PRINT,
    TOKEN_EOF
} TokenType;

typedef struct {
    TokenType type;
    char text[64];
} Token;

Token get_next_token();
void reset_lexer(const char *input);

typedef struct AST {
    enum { AST_NUM, AST_VAR, AST_BINOP, AST_ASSIGN, AST_PRINT } kind;
    union {
        int value;
        char name[64];
        struct {
            char op;
            struct AST *left;
            struct AST *right;
        };
        struct AST *expr;
    };
} AST;

AST *parse_statement();
void free_ast(AST *node);
int eval(AST *node);
void set_variable(const char *name, int value);
int get_variable(const char *name);

#endif
