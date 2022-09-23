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

logger = logging.getLogger(__name__)


class Protocol:
    """A simple example protocol demostrating how struct could be used
    to help manage the sending and recieving of messages.

    """

    def __init__(self):
        self.header_len = 4

    def send(self, sock, msg):
        """Formats the message for onward transmission. The first 4
        bytes are essentially the header and will contain the length
        of the message. This ensures we can do a socket.recv and
        get the entire message that was sent.
        """
        final_msg = struct.pack('>I', len(msg)) + msg.encode()
        logger.info("Sending the message: %s", final_msg)
        sock.sendall(final_msg)

    def recieve(self, sock):
        """Strips the 4 byte header and unpacks it in order to get
        the length of the message."""
        header = self.raw_receive(sock, self.header_len)
        logger.info("Recieved message header: %s", header)
        if not header:
            return None
        msg_len = struct.unpack('>I', header)[0]
        logger.info("Recieved message length: %s", msg_len)
        msg = self.raw_receive(sock, msg_len)
        logger.info("Recieved message: %s", msg)
        return msg.decode()

    def raw_receive(self, sock, msg_len):
        """Receives a specified amount fo data from the socket"""
        data = bytearray()
        while len(data) < msg_len:
            chunk = sock.recv(msg_len - len(data))
            if not chunk:
                return None
            data.extend(chunk)
        return data
