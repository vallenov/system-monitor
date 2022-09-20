from datetime import datetime


def datetime_dict():
    now = datetime.now()
    now_dict = {
        'second': now.second,
        'minute': now.minute,
        'hour': now.hour,
        'day': now.day,
        'month': now.month,
        'weekday': now.weekday(),
        'year': now.year
    }
    return now_dict
