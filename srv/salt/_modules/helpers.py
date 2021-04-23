def splitpart(value, index, char=','):
    if value is not None:
        return value.split(char)[index]
    return ''
