from os import path
import csv
from time import sleep
from datetime import datetime

from serial_wrapper import SerialWrapper, OpenPortException
from logger.logger import Logger


OUTPUT_PATH = path.join(path.dirname(path.abspath(__file__)), "output", "file.csv")

ACTIVITIES_MAP = {
    "1": "activity 1",
    "2": "activity 2",
    "3": "activity 3",
    "4": "activity 4",
    "5": "activity 5",
    "Stop": "NoActivity",
}


if __name__ == "__main__":
    logger = Logger(__name__)
    with SerialWrapper() as sw:
        activities = sw.activities
        try:
            while 1:
                sw.fetch_new_value()
                sleep(0.5)
        except KeyboardInterrupt as e:
            sw.stop()

    with open(OUTPUT_PATH, "w", newline="") as outfh:
        csv_writer = csv.writer(outfh, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(
            SerialWrapper.map_activities_for_export(activities, ACTIVITIES_MAP)
        )
