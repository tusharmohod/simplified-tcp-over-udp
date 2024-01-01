# A SIMPLIFIED VERSION OF TCP AS AN APPLICATION OVER UDP

Simplified simulated implementation of TCP (Transmission Control Protocol) on the application layer using UDP as a network layer protocol.

## Prerequisite

1. Unix/Linux based OS, MS Windows 10 and 11.
2. Python 3.
3. Netstat tool.

## How to install netstat tool

    $ sudo apt install net-tools         [On Debian/Ubuntu/Linux Mint]
    $ sudo yum install net-tools         [On RHEL/CentOS/Fedora]
    $ sudo emerge -a sys-apps/net-tools  [On Gentoo Linux]
    $ sudo apk add net-tools             [On Alpine Linux]
    $ sudo pacman -S net-tools           [On Arch Linux]
    $ sudo zypper install net-tools      [On OpenSUSE] 

## Cases covered

Two implementations are convered in this project:

1. Stop and Wait Protocol.
2. Go-Back-N ARQ Protocol.

## How to run

Stop and Wait Protocol.

    cd simplified-tcp-over-udp/
    cd stop-and-wait/

    # [in existing tab]
    python3 server -p PORT

    # [in other tab]
    python3 client -p PORT -s SEQUENCE_LIMIT

Go-Back-N ARQ Protocol.

    cd simplified-tcp-over-udp/
    cd go-back-n-arq/

    # [in existing tab]
    python3 server -p PORT

    # [in other tab]
    python3 client -p PORT -w WINDOW_SIZE -pl PACKETS_LIMIT   

## How to exit

Stop and Wait Protocol.  

    # Server
    # Press [Ctrl + C] to stop the server

    # Client
    # Either let the client complete or press [Ctrl + C] to stop the client

Go-Back-N ARQ Protocol.  

    # Server
    # Press [Ctrl + C] to stop the server

    # Client
    # Either let the client complete or press [Ctrl + C] to stop the client