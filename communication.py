# Communication class to deal with socket to the Siglent waveform generator.

import socket

class siglent_communication:
    """Deals with communication. In hindsight, do I really need a class for this?"""

    def __init__(self,ip,port):
        self._socket = socket.socket()
        self._socket.connect((ip,port))
        print(self._socket.recv(4096))

    def _send_and_receive(self,message):
        self._send(message)
        return self._receive()
        
    def _send(self,message):
        """Send the message, return the socket status."""
        return self._socket.send(bytes(message))
        
    def _receive(self):
        """Bit crude implementation, but it should work."""

        _msg = b""
        while True:
            if _msg[-1] == "\x00":
                break

            _msg += self._socket.recv(4096)

        return _msg
