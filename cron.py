from datetime import datetime
from functools import wraps
import re

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


def validate_rule(rule: str):
    """
    Check all rules before start app
    :param rule: rule like '0 0,30 */1 * * * *'
    :return: raise or None
    """
    rule_list = rule.split()
    if len(rule_list) != 7:
        raise ValueError(f'Rule length is not valid ({len(rule_list)})')
    res = re.search(r'^(\*\s|\*/\d+\s|\d+\s|(\d+,)+\d+\s){6}(\*|\*/\d+|\d+|(\d+,)+\d+)$', rule)
    if not res or not res.group(0):
        raise ValueError(f'Rule is not valid ({rule})')


def cron(rule: str = '* * * * * * *'):
    """
    Like linux cron
    '* * * * * * *' = every second
    '*/5 * * * * * *' = every 5 seconds
    '0 * * * * * *' = every minute
    '* * 0 * * * *' = every midnight
    '* * 0,12 * * * *' = every midnight and afternoon
    :param rule: rule of activation
    :return: decorator
    """
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            validate_rule(rule)
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
