import serial
from serial.serialutil import SerialException
from serial.tools import list_ports as list_serial_ports
from datetime import datetime

from time import sleep, time
from io import TextIOWrapper

from logger.logger import Logger

DEFAULT_BAUD_RATE = 9600
PORT_OPEN_TIMEOUT = 5


def coroutine(func):
    """Decorator to start coroutines"""

    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return primer


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
        self.logger = Logger(__name__)
        self.activities_list = []

        time_before_open = time()
        while not self.ser.isOpen():
            sleep(0.1)
            if time() + PORT_OPEN_TIMEOUT < time_before_open:
                raise OpenPortException(
                    f"reached timeout while trying to open port {arduino_port}"
                )
        self.logger.info(f"serial initialized with port: {arduino_port}")
        self.sio = TextIOWrapper(self.ser)

        self.coroutine = self.get_activity_coroutine()

    def read(self):
        """Read from arduino buffer"""
        if not self.ser.inWaiting():
            return None

        return self.sio.read()

    def _activity_coroutine(self):
        def extend_with_stop(activities_list: list):
            """Add stop data point"""
            activities_list.append({"activity": "Stop", "time": datetime.now()})
            return activities_list

        read_a_new_value = True
        while read_a_new_value:
            value = None
            read_a_new_value = yield value
            try:
                data_from_serial = self.read()
            except SerialException:
                return extend_with_stop(self.activities_list)
            if data_from_serial and data_from_serial != "\n":
                self.logger.debug(data_from_serial)
                value = {
                    "activity": data_from_serial,
                    "time": datetime.now(),
                }
                self.activities_list.append(value)

        return extend_with_stop(self.activities_list)

    def get_activity_coroutine(self):
        coroutine = self._activity_coroutine()
        next(coroutine)
        return coroutine

    def fetch_new_value(self):
        return self.coroutine.send(True)

    def stop(self):
        self.coroutine.send(False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ser.close()
        return True

    @property
    def activities(self):
        return self.activities_list

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

    @staticmethod
    def map_activities_for_export(activities: list, activities_map: dict):
        return map(
            lambda activity: (
                activities_map.get(activity.get("activity")),
                activity.get("time").strftime("%c"),
            ),
            activities,
        )


class OpenPortException(Exception):
    """Raised when the serial wrapper couldn't connect to the arduino serial port"""

    pass
