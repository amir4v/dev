import base64
from time import time
from django.http import HttpResponseBadRequest
from django.conf import settings


try:
    LIMIT = settings.THROTTLE_LIMIT
except:
    LIMIT = '2/4s' # 'Hit-Number/Number:(s/min/h/d/m/y)'

LIMIT_DURATION_s   = 1
LIMIT_DURATION_min = 60  *  LIMIT_DURATION_s
LIMIT_DURATION_h   = 60  *  LIMIT_DURATION_min
LIMIT_DURATION_d   = 24  *  LIMIT_DURATION_h
LIMIT_DURATION_m   = 30  *  LIMIT_DURATION_d
LIMIT_DURATION_y   = 365 *  LIMIT_DURATION_d

LIMIT_DURATION = {
    's': LIMIT_DURATION_s,
    'min': LIMIT_DURATION_min,
    'h': LIMIT_DURATION_h,
    'd': LIMIT_DURATION_d,
    'm': LIMIT_DURATION_m,
    'y': LIMIT_DURATION_y,
}


def set_limit(limit):
    global LIMIT
    LIMIT = limit


def get_limit():
    global LIMIT
    return LIMIT


def epoch():
    return int(time())


def expand_limit():
    hit_number, per = LIMIT.split('/')
    
    per = per.lower()
    if per.endswith('min'):
        per, duration = per[:-3], per[-3:]
    else:
        per, duration = per[:-1], per[-1:]
    
    return int(hit_number), int(per), duration


def encode(string):
        _bytes = base64.b64encode(string.encode('utf-8'))
        return _bytes
    
def decode(_bytes):
    string = base64.b64decode(_bytes).decode('utf-8')
    return string


# class CheckCookiesForThrottle:
#     def __init__(self, response):
#         self.response = response
    
#     def __call__(self, request):
#         response = self.response(request)
#         hit_number, per, duration = expand_limit()
#         throttle = request.COOKIES.get('throttle')
        
#         if throttle == None:
#             now = epoch()
#             total_duration = per * LIMIT_DURATION[duration]
#             until = now + total_duration
#             response.set_cookie('throttle', encode(f'1_{now}_{until}'))
        
#         return response


class Throttle:
    def __init__(self, response):
        self.response = response
    
    def __call__(self, request):
        response = self.response(request)
        hit_number, per, duration = expand_limit()
        throttle = request.COOKIES.get('throttle')
        
        if throttle == None:
            # return HttpResponseBadRequest()
            
            now = epoch()
            total_duration = per * LIMIT_DURATION[duration]
            until = now + total_duration
            response.set_cookie('throttle', encode(f'1_{now}_{until}'))
            
            return response
        
        throttle = throttle[2:-1]
        throttle = bytes(throttle.encode('utf-8'))
        throttle = decode(throttle)
        
        current_hit, _from, until = throttle.split('_')
        
        total_duration = per * LIMIT_DURATION[duration]
        current_hit = int(current_hit)
        _from = int(_from)
        until = int(until)
        
        now = epoch()
        if (now < until) and (current_hit >= hit_number):
            return HttpResponseBadRequest()
        elif now >= until:
            until = now + total_duration
            response.set_cookie('throttle', encode(f'1_{now}_{until}'))
        else:
            current_hit = current_hit + 1
            response.set_cookie('throttle', encode(f'{current_hit}_{_from}_{until}'))
        
        return response
