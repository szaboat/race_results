import time

def get_time_in_seconds(time_string):
    try:
        t = time.strptime(time_string, "%H:%M:%S")
        time_in_sec = t.tm_hour*60*60 + t.tm_min*60 + t.tm_sec
    except ValueError:
        time_in_sec = -1

    return time_in_sec
