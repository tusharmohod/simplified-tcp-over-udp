import socket
import sys
import argparse
import os
import signal

BUFFER_SIZE = 1024
ENCODING = "utf-8"

def handler(signum, frame):
    print(f"\nForce stoping the client ...")
    exit(0)


def send_packet(client_socket, sequence_number, conn):
    message = "Packet " + str(sequence_number)
    print(f"Sending Data: {message}")
    message = message.encode(ENCODING)
    client_socket.sendto(message, conn)
    received_message, address = client_socket.recvfrom(BUFFER_SIZE)
    received_message = received_message.decode(ENCODING)
    return received_message


def looper(sequence_number, sequence_limit, client_socket, conn, window_size, acked):
    while sequence_number <= sequence_limit:
        received_message = send_packet(client_socket, sequence_number, conn)
        if received_message == "Packet lost":
            print("-------------------------------------")
            print(f"Packet lost for sequence number: {sequence_number}")
            print(f"Packet sequence number from {len(acked) + 1} to {len(acked) + window_size} will be re-transmitted")
            print("-------------------------------------")
            looper(len(acked) + 1, min(sequence_limit, len(acked) + window_size),
                   client_socket, conn, window_size, acked)
            sequence_number += window_size
        else:
            sequence_number += 1
            print(f"Received ACK: {received_message}")
            acked.add(received_message.split(" ")[1])


def initialize_window(sequence_number, sequence_limit, client_socket, conn, window_size, acked):
    i = 1
    while i <= min(window_size, sequence_limit):
        message = "Packet " + str(sequence_number)
        print(f"Sending Data: {message}")
        message = message.encode(ENCODING)
        client_socket.sendto(message, conn)
        received_message, address = client_socket.recvfrom(BUFFER_SIZE)
        received_message = received_message.decode(ENCODING)
        if received_message == "Packet lost":
            print("-------------------------------------")
            print(f"Packet lost for sequence number: {sequence_number}")
            print(f"Packet sequence number from 1 to {len(acked)} will be re-transmitted")
            print("-------------------------------------")
            i = 1
            sequence_number = 1
        else:
            i += 1
            sequence_number += 1
            print(f"Received ACK: {received_message}")
            acked.add(received_message.split(" ")[1])


def client(port, window_size, sequence_limit):
    host = socket.gethostbyname(socket.gethostname())
    port = int(port)
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sequence_number = 1
    sequence_limit = int(sequence_limit)
    conn = (host, port)
    window_size = int(window_size)
    acked = set()

    try:
        is_valid_connection = os.system(f"netstat -tuln | grep :{port} > /dev/null 2>&1")
        if is_valid_connection != 0:
            raise ConnectionRefusedError

        initialize_window(sequence_number, sequence_limit, client_socket, conn, window_size, acked)
        sequence_number = window_size + 1
        looper(sequence_number, sequence_limit, client_socket, conn, window_size, acked)
        client_socket.sendto("Exit".encode(ENCODING), conn)
    except ConnectionRefusedError as e:
        print(f"No server running with port: {port}")
    except TimeoutError as e:
        print(f"Timeout raised")
    except IOError as e:
        print(f"IO Error")
    finally:
        if client_socket:
            client_socket.close()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    msg = "Sliding Window Protocol ARQ GO Back N Client Implementation"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("-p", "--port", help="The port number on which we want the client to communicate")
    parser.add_argument("-w", "--window_size", help="Sliding window size")
    parser.add_argument("-pl", "--packets_limit", help="The number of packets upto which the program will run")
    args = parser.parse_args()

    if not args.port:
        print("Provide a port number")
        print("Please check help for more information")
    elif not args.window_size:
        print("Provide a window size")
        print("Please check help for more information")
    elif not args.packets_limit:
        print("Provide packet limit size")
        print("Please check help for more information")
    else:
        client(args.port, args.window_size, args.packets_limit)
