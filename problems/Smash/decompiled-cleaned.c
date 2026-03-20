//  Cleaned decompiled.txt with help of LLM

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void say_hello(char *name) {
    char buf[128];

    strcpy(buf, name);

    printf("Hello, ");
    printf(buf);
    printf("!\n");
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    printf("What's your name?\n");

    char *name = NULL;
    size_t size = 0;
    int c;

    while ((c = getchar()) != '\n' && c != EOF) {
        char *tmp = realloc(name, size + 1);
        if (!tmp) {
            free(name);
            return 1;
        }
        name = tmp;
        name[size++] = (char)c;
    }

    char *tmp = realloc(name, size + 1);
    if (!tmp) {
        free(name);
        return 1;
    }
    name = tmp;
    name[size] = '\0';

    say_hello(name);

    free(name);
    return 0;
}