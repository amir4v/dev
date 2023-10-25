import string


def clean(value, strip=''):
    strip += string.whitespace
    if type(value) == str:
        value = value.strip(strip)
        if len(value) == 0:
            return None
        else:
            return value
    else:
        return value


def all_clean(iter, strip=''):
    if type(iter) in [list, tuple, set]:
        temp = []
        for i in iter:
            value = clean(i, strip)
            if value is not None:
                temp.append(value)
        return type(iter)(temp)
    elif type(iter) == dict:
        for k, v in iter:
            iter[k] = clean(v, strip)
        return iter
    else:
        return iter
