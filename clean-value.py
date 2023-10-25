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
    """Recursive"""
    if type(iter) not in [list, tuple, set, dict]:
        return clean(iter, strip)
    elif type(iter) in [list, tuple, set]:
        temp = []
        for i in iter:
            if type(i) not in [list, tuple, set, dict]:
                value = clean(i, strip)
            elif type(i) in [list, tuple, set, dict]:
                value = all_clean(i, strip)
            else:
                value = iter
            temp.append(value)
        return type(iter)(temp)
    elif type(iter) == dict:
        for k, v in iter.items():
            if type(v) not in [list, tuple, set, dict]:
                iter[k] = clean(v, strip)
            elif type(v) in [list, tuple, set, dict]:
                iter[k] = all_clean(v, strip)
            else:
                iter[k] = v
        return iter
    else:
        return iter
