from os import path
import csv
from time import sleep

from serial_wrapper import SerialWrapper

OUTPUT_PATH = path.join(path.dirname(path.abspath(__file__)), "output", "file.csv")


with SerialWrapper() as sw:
    while 1:
        data_from_serial = sw.read()
        if data_from_serial and data_from_serial != "\n":
            print(data_from_serial)
        sleep(1)
