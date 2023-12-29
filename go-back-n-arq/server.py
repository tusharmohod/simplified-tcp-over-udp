import socket
import random
import argparse
import signal


def handler(signum, frame):
    print(f"\nExiting the server ...")
    exit(0)


def server(port):
    BUFFER_SIZE = 1024
    ENCODING = "utf-8"
    host = socket.gethostbyname(socket.gethostname())
    port = int(port)
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # IPV4 and UDP connection
    conn = (host, port)

    try:
        server_socket.bind(conn)
        print(f"Server is up and running at port {port} ... ")

        while True:
            message, address = server_socket.recvfrom(BUFFER_SIZE)
            message = message.decode(ENCODING)
            if message == "Exit":
                continue
            if message:
                print(f" > {message}")
                sequence_number = message.split(" ")[1]
                print(f"Received Data: Packet {sequence_number}")
                print(f"Sending Ack: {message}")
                new_message = message.encode(ENCODING)
                num = random.randint(1, 10)
                if num == 4:
                    server_socket.sendto("Packet lost".encode(ENCODING), address)
                else:
                    server_socket.sendto(new_message, address)

    except OSError as e:
        print(f"Port {port} is already in use")
        print(e)
    finally:
        if server_socket:
            server_socket.close()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    msg = "Sliding Window Protocol ARQ GO Back N Client Implementation"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("-p", "--port", help="The port number on which the server will listen")
    args = parser.parse_args()

    if not args.port:
        print("Provide a port number")
        print("Please check help for more information")
    else:
        server(args.port)
