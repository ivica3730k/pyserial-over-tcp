import socket
import argparse
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] - %(message)s"
)
clients_list = []
clients_list_lock = threading.Lock()


def send_data_to_all(data):
    with clients_list_lock:
        for client_socket, _ in clients_list:
            client_socket.send(data.encode("utf-8"))
            logging.info(f"Sent data to {client_socket.getpeername()}: {data}")


def handle_connection(client_socket, address):
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        logging.info(f"Received data from {address}: {data}")
        if not data:
            logging.info(f"Client disconnected: {address}")
            with clients_list_lock:
                clients_list.remove((client_socket, address))
            break


def handle_socket():
    while True:
        client_socket, address = server_socket_listen_only_clients.accept()
        logging.info(f"Accepted connection from {address}")
        with clients_list_lock:
            clients_list.append((client_socket, address))
        client_thread = threading.Thread(
            target=handle_connection, args=(client_socket, address)
        )
        client_thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server for the serial port server.")
    parser.add_argument(
        "--port",
        type=int,
        default=12345,
        help="The port to listen on",
    )
    args = parser.parse_args()

    server_socket_listen_only_clients = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )
    server_socket_listen_only_clients.bind(("0.0.0.0", args.port))
    server_socket_listen_only_clients.listen(5)
    logging.info(f"Server listening for regular clients on port {args.port}")

    socket_handling_thread = threading.Thread(target=handle_socket)
    socket_handling_thread.start()

    while True:
        message = input("Enter message: ")
        send_data_to_all(message)
