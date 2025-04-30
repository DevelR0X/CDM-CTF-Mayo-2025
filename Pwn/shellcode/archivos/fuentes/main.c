#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>

typedef void (*ptr_exec)();

int main(int argc, char **argv){
    setbuf(stdout, NULL);

    size_t size = 128;
    size_t pagesize = sysconf(_SC_PAGESIZE);
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

    exec();
    
    munmap(mem, pagesize);
    return 0;
}