#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char **argv){
    char buf[32] = {0};
    char cmd[64] = {0};

    printf("Give me an argument: \n");

    read(0, buf, sizeof(buf)-1);
    snprintf(cmd, sizeof(cmd), "ls %s", buf);
    system(cmd);

    return 0;
}