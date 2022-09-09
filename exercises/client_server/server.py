import socket
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

def server(address, port):
    server_socket = socket.socket()
    server_socket.bind((address, port))
    server_socket.listen(2)
    logging.info("Waiting")
    conn, address = server_socket.accept()

    print(f"Connection from {address}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Data from connected user: {data}")
        data = input("->")
        conn.sendall(data.encode())

    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple server")
    parser.add_argument('-a', '--address', dest="address", default="", type=str, help="Address to Bind to")
    parser.add_argument('-p', '--port'   , dest="port"   , default=0 , type=int, help="Port to Bind to")
    args = parser.parse_args()

    server(args.address, args.port)

