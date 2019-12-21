import serial
from serial.tools import list_ports as list_serial_ports
from time import sleep
from io import TextIOWrapper
from os import path
import csv

OUTPUT_PATH = path.join(path.dirname(path.abspath(__file__)), "output", "file.csv")
BAUD_RATE = 9600

data_sent_in_serial = ""
last_data = ""

ports_used_by_arduino = list(
    filter(
        lambda comport: "arduino" in comport.description.lower(),
        [comport for comport in list_serial_ports.comports()],
    )
)

if len(ports_used_by_arduino) != 1:
    print(
        "Several ports for arduino found, could not choose"
        if len(ports_used_by_arduino) > 1
        else "No ports for arduino found"
    )
    exit()

arduino_port = ports_used_by_arduino[0].device

print(f"using port: {arduino_port}")

with serial.Serial(
    port=arduino_port,
    baudrate=BAUD_RATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2,
) as ser:

    while not ser.isOpen():
        sleep(0.1)
    print("serial initialized")
    sio = TextIOWrapper(ser)

    while 1:
        if ser.inWaiting() > 0:
            data_sent_in_serial = sio.read()
            if data_sent_in_serial != "\n":
                print(data_sent_in_serial)
        sleep(1)
