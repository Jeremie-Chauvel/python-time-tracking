from os import path
import csv
from time import sleep

from serial_wrapper import SerialWrapper
from logger.logger import Logger

OUTPUT_PATH = path.join(path.dirname(path.abspath(__file__)), "output", "file.csv")


def loop_read(logger=Logger(__name__)):
    with SerialWrapper() as sw:
        while 1:
            data_from_serial = sw.read()
            if data_from_serial and data_from_serial != "\n":
                logger.debug(data_from_serial)
            sleep(1)


if __name__ == "__main__":
    loop_read()

