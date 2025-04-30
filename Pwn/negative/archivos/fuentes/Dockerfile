FROM ubuntu:22.04
RUN apt-get update -y && apt-get install socat gcc -y
RUN addgroup --gid 1001 pown && adduser --uid 1001 --gid 1001 --shell /bin/sh --disabled-password pown
WORKDIR /home/pown
RUN mkdir -p ./app
WORKDIR /home/pown/app
COPY flag.txt .
COPY main.c .
RUN gcc -o server main.c
RUN chown -R pown:pown /home/pown/app
EXPOSE 1337
USER pown
CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./server"]