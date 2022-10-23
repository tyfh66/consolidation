"""Socket server that listens on a specified address and port. The server
waits for a client connection and forwards messages once connected."""
import socket
import logging
import argparse
from protocol import Protocol

class Server:
    """A very simple server that listens for incoming client connections
    whilst accepting user input. Uses the Protocol class to format messages,
    send and receive data.
    """

    def __init__(self, address: str, port: int) -> None:
        self.address = address
        self.port = port
        self.connections = []
        self.protocol = Protocol()

    def handle_user_connection(self, connection: socket.socket) -> None:
        """Loop that accepts user input then transmits that input to a
        connected client.
        """
        while True:
            try:
                msg = input("Send command to client:")
                if msg:
                    self.protocol.send(connection, msg)
                    recieved_msg = self.protocol.receive(connection)
                if recieved_msg:
                    logging.info("Received from client: %s", recieved_msg)

            except socket.error as comms_error:
                logging.error(
                    "Transmission error: %s", comms_error)
                self.remove_connection(connection)
                break

    def remove_connection(self, conn: socket.socket) -> None:
        """Removes a socket from the list of connected sockets."""
        if conn in self.connections:
            conn.close()
            self.connections.remove(conn)

    def run(self) -> None:
        """Sets up the server socket and listens for incoming client
        connections.
        """
        try:
            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as socket_error:
            logging.error("Error %s initialising socket", socket_error)

        socket_instance.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            socket_instance.bind(('', self.port))
            socket_instance.listen(1)
            logging.info('server running')
        except socket.error as socket_error:
            logging.error('Error %s binding socket.', socket_error)
            socket_instance.close()

        while True:
            socket_connection, address = socket_instance.accept()
            logging.info("Client connected: %s", address)
            self.connections.append(socket_connection)
            self.handle_user_connection(socket_connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple server")
    parser.add_argument('-a', '--address', dest="address",
                        default="", type=str, help="Address to Bind to")
    parser.add_argument('-p', '--port', dest="port",
                        default=0, type=int, help="Port to Bind to")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    server = Server(args.address, args.port)
    server.run()
