import re
from collections import OrderedDict


def splitpart(value, index, char=','):
    if value is not None:
        return value.split(char)[index]
    return ''


def parse_debver(value):
    try:
        return re.findall(r"(?:\d+:)?([^~]+)", value)[0]
    except:
        return ''


def deep_sort(obj):
    if isinstance(obj, dict):
        obj = OrderedDict(sorted(obj.items()))
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                obj[k] = deep_sort(v)
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict) or isinstance(v, list):
                obj[i] = deep_sort(v)
        obj = sorted(obj, key=lambda x: json.dumps(x))
    return obj
