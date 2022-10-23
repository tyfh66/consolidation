""" A client 'agent'. The client runs on a remote host
and uses a socket connection to connected to hardcoded
address and port."""
import socket
import sys
import logging
from protocol import Protocol


class Client:
    """A simple client which can be run a remote host. Client
    will connect to a given ip addr and port and responds to
    messages by echoing them back to the server.
    """

    def __init__(self, ip_address: str, port: int) -> None:
        self.server_address = ip_address
        self.server_port = port
        self.running = True
        self.protocol = Protocol()

    def terminate_client(self, connection: socket.socket) -> None:
        """Terminate and close the connection, terminate the client."""
        connection.close()
        self.running = False
        logging.warning("Client is terminating.")
        sys.exit(1)

    def handle_messages(self, connection: socket.socket) -> None:
        """Uses the Protocol class to receive a message then
        respond to the server that sent it with the same message.
        """
        while self.running:
            try:
                cmd = self.protocol.receive(connection)
                if cmd:
                    if cmd == 'exit':
                        self.terminate_client(connection)
                    self.protocol.send(connection, cmd)
                else:
                    self.terminate_client(connection)
            except socket.error as comms_error:
                logging.error(
                    "Error handling message from server: %s", comms_error)
                self.terminate_client(connection)

    def run(self) -> None:
        """Creates the socket instance and enters the handle messages
        loop.
        """
        try:
            socket_instance = socket.socket()
            socket_instance.connect((self.server_address, self.server_port))
            socket_instance.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as connection_error:
            logging.error("Error connecting to server socket: %s",
                          connection_error)
            socket_instance.close()
            sys.exit(1)

        self.handle_messages(socket_instance)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = Client("127.0.0.1", 12000)
    client.run()
