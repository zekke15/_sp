#include <string.h>
#include <stdlib.h>

typedef struct {
字元名稱[64];
整數值；
} 變數；

靜態變數 vars[100];
static int var_count = 0;

void set_variable(const char *name, int value) {
for (int i = 0; i < var_count; i++) {
如果 (strcmp(vars[i].name, name) == 0) {
vars[i].value = value;
返回;
}
}
strcpy(vars[var_count].name, 名稱);
vars[var_count].value = 值；
var_count++;
}

int get_variable(const char *name) {
for (int i = 0; i < var_count; i++) {
如果 (strcmp(vars[i].name, name) == 0) {
返回 vars[i].value;
}
}
返回 0；
}