import socket
import argparse
import signal
import os


def handler(signum, frame):
    print(f"\nForce stoping the client ...")
    exit(0)


def client_program(port, sequence_limit):
    BUFFER_SIZE = 1024
    ENCODING = "utf-8"
    host = socket.gethostbyname(socket.gethostname())
    port = int(port)
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # IPV4 and UDP connection
    sequence_number = 1
    sequence_limit = int(sequence_limit)

    try:
        is_valid_connection = os.system(f"netstat -tuln | grep :{port} > /dev/null 2>&1")
        if is_valid_connection != 0:
            raise ConnectionRefusedError

        conn = (host, port)
        print(f"client is connected at port {port} ... ")
        while sequence_number <= sequence_limit:
            message = "Packet " + str(sequence_number)
            print(f"Sending Data: {message}")
            message = message.encode(ENCODING)
            client_socket.sendto(message, conn)
            received_message, address = client_socket.recvfrom(BUFFER_SIZE)
            received_message = received_message.decode(ENCODING)
            if received_message != "Packet lost":
                sequence_number += 1
                print(f"Received ACK: {received_message}")
            else:
                print("-------------------------------------")
                print(f"Packet lost")
                print("-------------------------------------")
        # client_socket.sendto("Exit".encode(ENCODING), conn)
    except ConnectionRefusedError as e:
        print(f"No server running with port: {port}")
    except TimeoutError as e:
        print(f"Timeout raised")
        print(e)
    except IOError as e:
        print(f"IO Error")
        print(e)
    finally:
        if client_socket:
            client_socket.close()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    msg = "Sliding Window Protocol Stop and Wait Client Implementation"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("-p", "--port", help = "The port number on which we want client to communicate")
    parser.add_argument("-s", "--sequence_limit", help = "The maximum number of packets to be processed")
    args = parser.parse_args()

    if not args.port:
        print(f"Provide a port number")
        print(f"Check help for more information")
    elif not args.sequence_limit:
        print(f"Provide a sequence limit")
        print(f"Check help for more information")
    else:
        client_program(args.port, args.sequence_limit)