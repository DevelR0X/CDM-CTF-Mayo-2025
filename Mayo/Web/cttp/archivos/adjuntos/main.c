#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define MENU "Endpoint list:\n \
1. GET /file\n \
 -args: filename=<name>\n \
Example: \n\
GET /file&filename=myfile.txt\n \
FLAG path /root/flag.txt"

int main(int argc, char **argv){

    char buf[1024] = {0}, tmp[1024] = {0};
    
    int valid = 0;
    for (int i = 0; i < sizeof(buf); i++){
        read(0, buf + i, 1);
        if (i > 3 && buf[i-3] == '\r' && buf[i-2] == '\n' && buf[i-1] == '\r' && buf[i] == '\n'){
            valid = 1;
            break;
        }
    }

    if (!valid){
        printf("Dirty cheater\n");
    }

    char *line = strstr(buf, " ");
    if (!line){
        printf("Dirty Cheater");
        return 1;
    }

    char *line2 = strstr(line+1, " ");
    if (!line2){
        printf("Dirty Cheater");
        return 1;
    }

    char path[64] = {0};
    strncpy(path, line + 1, line2 - line - 1);

    if (!strncmp("/file", path, 5)){
        char *args = strstr(path, "&");
        if (!args){
            printf("Dirty cheater\n");
            return 1;
        }

        char *value = strstr(args + 1, "=") + 1;
        if (!value){
            printf("Dirty cheater\n");
            return 1;
        }

        if (value[0]=='/'){
            printf("Dirty cheater\n");
            return 1;
        }

        char key[16]={0};
        strncpy(key, args+1, value-args - 2);

        FILE *file = fopen(value, "r");
        if (!file){
            printf("Dirty cheater\n");
            return 1;
        }

        char contents[128] = {0};
        fread(contents, 1, sizeof(contents)-1, file);
        printf("%s\n", contents);

    }else if(!strcmp("/", path)){
        printf("%s\n", MENU);
    }else{
        printf("Dirty cheater\n");
    }

    return 0;
}