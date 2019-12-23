from datetime import datetime, timedelta
from os import path
import csv


def get_time_frames_from_data_points(data_points: list):
    """Return an erray of activities time frames

    Convert:                                                 Into:
    [                                                        [
        {'activity': '1', 'time': time1Obj},                     {'activity': '1', 'delta': timedelta(time1Obj, time2Obj)},
        {'activity': '5', 'time': time2Obj},                     {'activity': '5', 'delta': timedelta(time2Obj, time4Obj)},
        {'activity': '5', 'time': time3Obj},                     {'activity': '3', 'delta': timedelta(time4Obj, time5Obj)}
        {'activity': '3', 'time': time4Obj},                 ]
        {'activity': 'Stop', 'time': time5Obj}
    ]
    """
    if len(data_points) < 2:
        raise DataPointsToTimeFramesConversionException(
            "Not enought data points, less than 2 were given"
        )

    time_frames = [{"activity": data_points[0].get("activity"), "delta": timedelta()}]
    for index in range(1, len(data_points)):
        previous_data_point, current_data_point = data_points[index - 1 : index + 1]
        previous_activity = previous_data_point.get("activity")
        current_activity = current_data_point.get("activity")

        time_frames[-1] = {
            "activity": previous_activity,
            "delta": time_frames[-1].get("delta")
            + (current_data_point.get("time") - previous_data_point.get("time")),
        }

        if current_activity != "Stop" and previous_activity != current_activity:
            time_frames.append({"activity": current_activity, "delta": timedelta()})

    return time_frames


def pretty_print_activities(activities: list):
    import pprint

    def format_activity(activity_object):
        try:
            return {
                "activity": activity_object.get("activity"),
                "time": activity_object.get("time").strftime("%X"),
            }
        except AttributeError:
            return {
                "activity": activity_object.get("activity"),
                "delta": activity_object.get("delta").total_seconds(),
            }

    pprint.PrettyPrinter(indent=4).pprint(list(map(format_activity, activities)))


class DataPointsToTimeFramesConversionException(Exception):
    pass


if __name__ == "__main__":
    with open(
        path.join(path.dirname(path.abspath(__file__)), "output", "file.csv"), "r"
    ) as infh:
        csv_reader = csv.reader(infh, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        activities = [
            {"activity": k[0], "time": datetime.strptime(k[1], "%c")}
            for k in csv_reader
        ]

    pretty_print_activities(activities)
    time_frames = get_time_frames_from_data_points(activities)
    print("Converted into:")
    pretty_print_activities(time_frames)
