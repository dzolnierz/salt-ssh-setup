import re


def splitpart(value, index, char=','):
    if value is not None:
        return value.split(char)[index]
    return ''


def parse_debver(value):
    try:
        return re.findall(r"(?:\d+:)?(.*)~", value)[0]
    except:
        return ''
