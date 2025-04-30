#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct client_info{
    char name[16];
    char surname[16];
    struct client_info *next;
    char admin;
};

int main(int argc, char **argv){
    setbuf(stdout, NULL);
    
    char flag[64]= {0};
    FILE *file = fopen("flag.txt", "r");
    fread(flag, 1, 64, file);

    int num_clients = 0;
    struct client_info client_list = {0};
    struct client_info *curr = 0;

    while(1){
        struct client_info *client = 0;
        int opt = 0;
        printf("1. New client\n2. Print client list\n3. Write review \n4. Give me the flag\n5. Exit\n> \n");
        scanf("%d",&opt);

        switch(opt){
            case 1:
                if (num_clients == 0)
                    client = &client_list;
                else
                    client = malloc(sizeof(struct client_info));
                printf("Username: \n");
                read(STDIN_FILENO, client->name, sizeof(client->name));
                printf("Surname: \n");
                read(STDIN_FILENO, client->surname, sizeof(client->surname));

                client->next = curr;
                curr = client;
                
                num_clients++;
            break;

            case 2:
                if (!num_clients){
                    printf("Add some clients first\n");
                    continue;
                }
                client = curr;
                do{
                    printf("Name: %s\nSurname: %s\n", client->name, client->surname);
                    client = client->next;
                }while(client);
            break;

            case 3:
                printf("Write a review in memory\n");
                printf("Give me a hexadecimal address: \n");

                unsigned long addr = 0;
                scanf("%llx", &addr);
                unsigned long *ptr = (unsigned long*)addr;
                *ptr = 1;
                
            break;

            case 4:
                if (!num_clients){
                    printf("Add some clients first\n");
                    continue;
                }
                client = curr;
                do{
                    if (client->admin == 0x1){
                        printf("%s\n", flag);
                        return 0;
                    }
                    client = client->next;
                }while(client);

                printf("Better luck next time\n");
                
            break;

            case 5:
                printf("Goodbye!\n");
                exit(-1);
            break;

            default:
                printf("Wrong option.\n");

            break;
        }

    }

    return 0;
}