import serial
from serial.tools import list_ports as list_serial_ports
from time import sleep, time

from io import TextIOWrapper


DEFAULT_BAUD_RATE = 9600
PORT_OPEN_TIMEOUT = 5


class SerialWrapper:
    def __init__(self, baud_rate=DEFAULT_BAUD_RATE):
        arduino_port = SerialWrapper.get_arduino_com_port()

        self.ser = serial.Serial(
            port=arduino_port,
            baudrate=baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2,
        )

        time_before_open = time()
        while not self.ser.isOpen():
            sleep(0.1)
            if time() + PORT_OPEN_TIMEOUT < time_before_open:
                raise OpenPortException(
                    f"reached timeout while trying to open port {arduino_port}"
                )
        print(f"serial initialized with port: {arduino_port}")
        self.sio = TextIOWrapper(self.ser)

    def read(self):
        """Read from arduino buffer"""
        if not self.ser.inWaiting():
            return None

        return self.sio.read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ser.close()
        return True

    @staticmethod
    def get_arduino_com_port():
        ports_used_by_arduino = list(
            filter(
                lambda comport: "arduino" in comport.description.lower(),
                [comport for comport in list_serial_ports.comports()],
            )
        )

        if len(ports_used_by_arduino) != 1:
            raise OpenPortException(
                "Several ports for arduino found, could not choose"
                if len(ports_used_by_arduino) > 1
                else "No ports for arduino found"
            )

        return ports_used_by_arduino[0].device


class OpenPortException(Exception):
    """Raised when the serial wrapper couldn't connect to the arduino serial port"""

    pass
