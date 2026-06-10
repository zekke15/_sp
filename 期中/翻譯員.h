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
        int value;              // AST_NUM
        char name[64];          // AST_VAR or AST_ASSIGN
        struct {                // AST_BINOP
            char op;
            struct AST *left;
            struct AST *right;
        };
        struct AST *expr;       // AST_PRINT
    };
} AST;

AST *parse_statement();
void free_ast(AST *node);
int eval(AST *node);
void set_variable(const char *name, int value);
int get_variable(const char *name);

#endif