import string

from django.utils.deprecation import MiddlewareMixin


class CleanMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.POST._mutable = True
        request.GET._mutable = True
        
        temp_POST = all_clean(dict(request.POST))
        for k, v in temp_POST.items():
            if len(v) == 1 and type(v) != str:
                temp_POST[k] = v[0]
        
        temp_GET = all_clean(dict(request.GET))
        for k, v in temp_GET.items():
            if len(v) == 1 and type(v) != str:
                temp_GET[k] = v[0]
        
        for k, v in temp_POST.items():
            request.POST.__setitem__(k, v)
        
        for k, v in temp_GET.items():
            request.GET.__setitem__(k, v)


def exists(value):
    try:
        if      value is None or \
                clean(value) is None or \
                len(value) == 0 or \
                len(clean(value)) == 0:
            return False
        else:
            return True
    except:
        return True


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


def all_clean(iter, strip='', strict=True):
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
            if not strict:
                temp.append(value)
            elif strict and exists(value):
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
            if strict and not exists(iter[k]):
                # del iter[k]
                iter[k] = None
        return iter
    else:
        return iter
