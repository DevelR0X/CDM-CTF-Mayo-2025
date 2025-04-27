#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>

u_char blacklist[] = "\x58\x50\x5f\x58\x5e\x5d\x5a\x59";

size_t size = 128;
size_t pagesize = 0;

typedef void (*ptr_exec)();

int check_list(u_char *buff){
    for(int i = 0; i < sizeof(blacklist)-1; i++){
        for(int j = 0; j < size; j++){
            if (buff[j] == blacklist[i]){
                return 0;
            }
        }
    }

    return 1;
}

int main(int argc, char **argv){
    pagesize = sysconf(_SC_PAGESIZE);

    void *mem = mmap(NULL, pagesize, PROT_READ | PROT_WRITE, 
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
                     
    if (mem == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    if (mprotect(mem, pagesize, PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        perror("mprotect");
        return 1;
    }

    printf("give me a shellcode: \n");
    
    read(STDIN_FILENO, mem, size);
    
    ptr_exec exec = (ptr_exec)mem;

    if (check_list((u_char*)mem)){
        exec();
    }else{
        printf("Try harder\n");
    }

    munmap(mem, pagesize);
    return 0;
}