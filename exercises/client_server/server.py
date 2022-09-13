import socket
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

HEADER_LENGTH = 8

def send_msg(msg_text):
    full_msg = f"{len(msg_text):<{HEADER_LENGTH}}" + msg_text
    return full_msg.encode()

def recieve(sock):   
    msg_header = sock.recv(HEADER_LENGTH)
    if not len(msg_header):
        return False
    msg_len = int(msg_header.decode().strip())
    data = sock.recv(msg_len).decode()
    logging.info(f"[*] Data from connected hostname:\n{data}")
    return data  

def client_connect(server_socket):
    client_socket, client_addr = server_socket.accept()
    logging.info(f"[*] Connection from: {client_addr}")
    return client_socket

def server(address, port): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((address, port))
        server_socket.listen(1)    
        client_socket = client_connect(server_socket)
    
        while True:
            user_input = input("Waiting for input:")
            data = send_msg(user_input)
            client_socket.send(data)
            data = recieve(client_socket) 
            if not data:
                logging.error("[*] Error")                
                client_socket = client_connect(server_socket)       

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple server")
    parser.add_argument('-a', '--address', dest="address", default="", type=str, help="Address to Bind to")
    parser.add_argument('-p', '--port'   , dest="port"   , default=0 , type=int, help="Port to Bind to")
    args = parser.parse_args()

    server(args.address, args.port)

