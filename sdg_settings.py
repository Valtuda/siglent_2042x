# Settings library for siglent 2042x waveform generator. We will only implement DC (for now).

from .sdg_communication import sdg_communication

class sdg_settings:
    """Exposes some of the settings of the waveform generator."""
    def __init__(self,ip,port,max_voltage = 5):
        self._max_voltage = max_voltage

        self._communication = sdg_communication(ip,port)

        # Reset doesn't automatically turn off the output, and we don't want to damage anything.
        self.output(False)

        self.reset()
        self.clear_errors()
        self.set_limits()

        self.set_voltage(1,0)
        self.set_voltage(2,0)

        self.output(True)

    def reset(self):
        self._communication.send_and_receive("*RST")

    def clear_errors(self):
        self._communication.send_and_receive("*CLS")

    def output(self,status,ch=0):
        if ch not in [0,1,2]:
            raise ValueError("Channel must be 1 or 2, or 0 for both.")
        if status not in [True,False]:
            raise ValueError("Output must be True or False.")

        if status:
            command = "ON"
        else:
            command = "OFF"

        if ch == 0:
            self.output(status,1)
            self.output(status,2)
        else:
            self._communication.send_and_receive(f"C{ch}:OUTP ON,LOAD,HZ")

    def set_voltage(self,ch,voltage):
        if ch not in [1,2]:
            raise ValueError("Channel must be 1 or 2.")
        if voltage < -self._max_voltage or voltage > self._max_voltage:
            raise ValueError("Voltage must be between -5 and +5 V.")

        self._communication.send_and_receive(f"C{ch}:BSWV WVTP,DC,OFST,{voltage}")
