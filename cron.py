from datetime import datetime
from functools import wraps

date_format = ['second', 'minute', 'hour', 'day', 'month', 'weekday', 'year']


def cron(rule: str = '* * * * * * *'):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            rule_list = rule.split()
            if len(rule_list) != 7:
                raise ValueError('Wrong rule')
            rule_dict = dict(zip(date_format, rule_list))
            now = datetime.now()
            rule_dict['second'] = now.second if rule_dict['second'] == '*' else int(rule_dict['second'])
            rule_dict['minute'] = now.minute if rule_dict['minute'] == '*' else int(rule_dict['minute'])
            rule_dict['hour'] = now.hour if rule_dict['hour'] == '*' else int(rule_dict['hour'])
            rule_dict['day'] = now.day if rule_dict['day'] == '*' else int(rule_dict['day'])
            rule_dict['month'] = now.month if rule_dict['month'] == '*' else int(rule_dict['month'])
            rule_dict['weekday'] = now.weekday() if rule_dict['weekday'] == '*' else int(rule_dict['weekday'])
            rule_dict['year'] = now.year if rule_dict['year'] == '*' else int(rule_dict['year'])
            now_dict = {
                'second': now.second,
                'minute': now.minute,
                'hour': now.hour,
                'day': now.day,
                'month': now.month,
                'weekday': now.weekday(),
                'year': now.year
            }
            if rule_dict == now_dict:
                return func(*args, **kwargs)
        return wrap
    return decorator
