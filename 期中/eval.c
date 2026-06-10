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