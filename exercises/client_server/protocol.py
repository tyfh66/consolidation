"""A trivial example of how a simple message 'protocol' could be handled. 
In this case we use a simple fixed 4 byte header which will contain the
length of the message. There are many other ways to format a message, this
is just an example. Another one would be something like 
struct.pack('>Ii', len(msg_text), int(op_code)) + msg_text.encode()
This would make the header 8 bytes and would contain the length of
the message, some numerical code to signify a specific command and any
other data. """

import struct
import logging
import socket
import sys

logger = logging.getLogger(__name__)

class Protocol:
    """A simple example protocol demostrating how struct could be used
    to help manage the sending and receiving of messages.

    """

    def __init__(self):
        self.header_len = 4

    def send(self, sock: socket.socket, msg: str) -> None:
        """Formats the message for onward transmission. The first 4
        bytes are essentially the header and will contain the length
        of the message. This ensures we can do a socket.recv and
        get the entire message that was sent.
        """
        final_msg = struct.pack('>I', len(msg)) + msg.encode()
        logger.info("Sending the message: %s", final_msg)
        sock.sendall(final_msg)

    def receive(self, sock: socket.socket) -> str:
        """Strips the 4 byte header and unpacks it in order to get
        the length of the message."""
        header = self.raw_receive(sock, self.header_len)
        logger.info("Received message header: %s", header)
        msg_len = struct.unpack('>I', header)[0]
        logger.info("Received message length: %s", msg_len)
        msg = self.raw_receive(sock, msg_len)
        logger.info("Received message: %s", msg)
        return msg.decode()

    def raw_receive(self, sock: socket.socket, msg_len: int) -> bytearray:
        """Receives a specified amount fo data from the socket"""
        data = bytearray()
        while len(data) < msg_len:
            try:
                chunk = sock.recv(msg_len - len(data))
                data.extend(chunk)
            except socket.error as error_message:
                print("Error receiving data: %s", error_message)
                sys.exit(1)
        return data
