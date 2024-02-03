import socket
import argparse
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] - %(message)s"
)

def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        logging.info(f"Received data: {data}")

def send_data(client_socket):
    while True:
        message = input("Enter message: ")
        client_socket.send(message.encode("utf-8"))
        logging.info(f"Sent data: {message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for the serial port server.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The server's IP address or hostname",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=12345,
        help="The port to connect to",
    )
    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.host, args.port))
    logging.info(f"Connected to server at {args.host}:{args.port}")

    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    send_thread = threading.Thread(target=send_data, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()
