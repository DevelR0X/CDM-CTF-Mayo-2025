#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char **argv){
    char buff[16] = {0};
    char flag[64] = {0};
    
    FILE *file = fopen("flag.txt", "r");
    if (!file){
        printf("no flag.txt present, create one\n");
        exit(-1);
    }
    
    fread(flag, 1, 64, file);
    
    printf("Enter some input: \n");

    read(STDIN_FILENO, buff, sizeof(buff));

    printf("Your input is: %s\n", buff);

    return 0;
}