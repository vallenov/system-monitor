from datetime import datetime
from functools import wraps

date_format = ['second', 'minute', 'hour', 'day', 'month', 'weekday', 'year']


class CronDict(dict):
    def __eq__(self, other: dict):
        for key, value in self.items():
            if other.get(key) is None:
                return False
            if isinstance(value, int):
                if value != int(other[key]):
                    return False
            elif isinstance(value, list):
                if '*' in value:
                    if other[key] % value[1]:
                        return False
                else:
                    if other[key] not in value:
                        return False
        return True


def cron(rule: str = '* * * * * * *'):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            rule_list = rule.split()
            if len(rule_list) != 7:
                raise ValueError('Wrong rule')
            rule_dict = CronDict(zip(date_format, rule_list))
            now_dict = kwargs.get('now_dict')
            if not now_dict:
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
            for key, value in now_dict.items():
                if rule_dict[key] == '*':
                    rule_dict[key] = value
                elif '*' in rule_dict[key]:
                    rule_dict[key] = list(map(lambda x: int(x) if x != '*' else x, rule_dict[key].split('/')))
                elif ',' in rule_dict[key]:
                    try:
                        rule_dict[key] = list(map(lambda x: int(x), rule_dict[key].split(',')))
                    except ValueError:
                        raise ValueError('Wrong rule')
                elif len(rule_dict[key]) == 1:
                    try:
                        rule_dict[key] = int(rule_dict[key])
                    except ValueError:
                        raise ValueError('Wrong rule')
                else:
                    raise ValueError('Wrong rule')
            if rule_dict == now_dict:
                return func(*args, **kwargs)
        return wrap
    return decorator
