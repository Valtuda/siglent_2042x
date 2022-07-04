# Communication class to deal with socket to the Siglent waveform generator.

import socket

class siglent_communication:
    """Deals with communication. In hindsight, do I really need a class for this?"""

    def __init__(self,ip,port):
        self._socket = socket.socket()
        self._socket.connect((ip,port))
        self._socket.recv(4096) # Eat the connection message.

    def send_and_receive(self,message):
        self.send(message)
        return self.receive()
        
    def send(self,message):
        """Send the message, return the socket status."""
        return self._socket.send(bytes(message)+b"\r\n")
        
    def receive(self):
        """Bit crude implementation, but it should work."""

        _msg = b""
        while True:
            if len(_msg) > 0 and _msg[-1] == "\x00":
                break

            _msg += self._socket.recv(4096)
            print(_msg)

        return _msg
