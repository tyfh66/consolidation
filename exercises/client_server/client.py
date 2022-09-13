import socket
import time
import logging
from commands import get_time

logging.basicConfig(level=logging.DEBUG)

HEADER_LENGTH = 8

class Client:
    def __init__(self, _ip, _port):
        self._ip = _ip
        self._port = _port
        self.sock = None
        self.hostname = None

    def send_msg(self, msg_text):
        full_msg = f"{len(msg_text):<{HEADER_LENGTH}}" + msg_text
        return full_msg.encode()

    def initialise_socket(self):
        self.hostname = socket.gethostname()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def process_command(self, message):
        if message == "time":
            logging.info(f"[*] Recieved the {message} command.")
            self.sock.sendall(self.send_msg(get_time()))
        else:
            self.sock.sendall(self.send_msg("garbage command"))

    def recieve(self):
        while True:            
            msg_header = self.sock.recv(HEADER_LENGTH)
            if not len(msg_header):
                break
            msg_len = int(msg_header.decode().strip())            
            data = self.sock.recv(msg_len).decode()
            self.process_command(data)        

    def run(self):
        self.initialise_socket()        
        while True:
            try:                
                logging.info(f"[*] Attempting connection to: {self._ip} {self._port}")
                self.sock.connect((self._ip, self._port))
                logging.info("[*] Connected.")                
            except:
                logging.error("[*] Failed to connect, trying again.")
                self.initialise_socket()
                time.sleep(5)
                continue

            self.recieve()   


if __name__ == '__main__':
    client = Client("127.0.0.1", 1234)
    client.run()
