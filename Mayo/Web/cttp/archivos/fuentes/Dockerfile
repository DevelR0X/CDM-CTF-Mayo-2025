FROM ubuntu:22.04
RUN apt-get update -y && apt-get install socat gcc -y
RUN addgroup --gid 1001 pown && adduser --uid 1001 --gid 1001 --shell /bin/sh --disabled-password pown
WORKDIR /
COPY flag.txt flag.txt
RUN chown pown:pown /flag.txt
WORKDIR /home/pown
RUN mkdir -p ./app
WORKDIR /home/pown/app
COPY main.c .
RUN gcc -o server main.c
RUN chown -R pown:pown /home/pown/app
RUN chmod u=r,g=r,o= /flag.txt
EXPOSE 1337
USER pown
CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./server"]