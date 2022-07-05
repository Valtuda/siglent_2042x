# Communication class to deal with socket to the Siglent waveform generator.

import socket

class sdg_communication:
    """Deals with communication. In hindsight, do I really need a class for this?"""

    def __init__(self,ip,port,timeout=10):
        self._socket = socket.socket()
        self._socket.connect((ip,port))
        self._socket.settimeout(timeout)
        try:
            self._socket.recv(4096) # Eat the connection message.
        except:
            pass # If there is no message, we might have been previously connected, don't crap out on this.

    def send_and_receive(self,message):
        self.send(message)
        return self.receive()
        
    def send(self,message):
        """Send the message, return the socket status."""
        return self._socket.send(bytes(message,'utf-8')+b"\r\n")
        
    def receive(self):
        """Bit crude implementation, but it should work."""

        _msg = b""
        while not (len(_msg)>0 and _msg[-1]==0):
            _msg += self._socket.recv(4096)

        return _msg
