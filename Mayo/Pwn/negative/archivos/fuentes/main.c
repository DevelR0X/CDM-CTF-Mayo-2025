#include <stdio.h>

char admin = 0;
char buffer[64] = {0};

int main(int argc, char **argv){
    setbuf(stdout, NULL);

    char flag[64] = {0};
    FILE *file = fopen("flag.txt", "r");
    fread(flag, 1, 64, file);

    __uint32_t pos = 0;

    printf("Position to write in the buffer: \n");

    scanf("%d", &pos);
    
    if (pos > 0){
        char offset = 0x10;
        char sum = (char)(pos+offset);
        buffer[sum] = 1;
    }

    if (admin){
        printf("Congratulations here's the flag: %s\n", flag);
    }else{
        printf("Try harder\n");
    }

    return 0;
}