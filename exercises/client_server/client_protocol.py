import socket
import logging
from protocol import Protocol


class Client:
    """A simple client which can be run a remote host. Client
    will connect to a given ip addr and port and responds to
    messages by echoing them back to the server.
    """

    def __init__(self, ip_address, port):
        self.server_address = ip_address
        self.server_port = port
        self.protocol = Protocol()

    def handle_messages(self, connection: socket.socket):
        """Uses the Protocol class to recieve a message then
        respond to the server that sent it with the same message.
        """
        while True:
            try:
                cmd = self.protocol.recieve(connection)
                if cmd:
                    self.protocol.send(connection, cmd)
                else:
                    connection.close()
                    break
            except socket.error as comms_error:
                logging.error(
                    "Error handling message from server: %s", comms_error)
                connection.close()
                break

    def run(self):
        """Creates the socket instance and enters the handle messages
        loop.
        """
        try:
            socket_instance = socket.socket()
            socket_instance.connect((self.server_address, self.server_port))
            socket_instance.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.handle_messages(socket_instance)

        except socket.error as connection_error:
            logging.error("Error connecting to server socket: %s",
                          connection_error)
            socket_instance.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = Client("127.0.0.1", 12000)
    client.run()
