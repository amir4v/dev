import base64
from time import time
from django.http import HttpResponseBadRequest
from django.conf import settings
from .models import Memory, View, ViewMemory


try:
    LIMIT = settings.THROTTLE_LIMIT
except:
    LIMIT = '1/2s' # 'Hit-Number/Number:(s/min/h/d/m/y)'

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


def expand_limit(limit=None):
    if limit:
        hit_number, per = limit.split('/')
    else:
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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def throttle_split(throttle):
    current_hit, _from, until = throttle.split('_')
    return int(current_hit), int(_from), int(until)


class ThrottleMiddleware:
    def __init__(self, response):
        self.response = response
    
    def __call__(self, request):
        ip = get_client_ip(request)
        response = self.response(request)
        hit_number, per, duration = expand_limit()
        
        # throttle = request.COOKIES.get('throttle')
        memory, created = Memory.objects.get_or_create(ip=ip)
        
        if created:
            # return HttpResponseBadRequest()
            now = epoch()
            total_duration = per * LIMIT_DURATION[duration]
            until = now + total_duration
            # response.set_cookie('throttle', encode(f'1_{now}_{until}'))
            memory.throttle = encode(f'1_{now}_{until}')
            memory.save()
            
            return response
        else:
            throttle = memory.throttle
        
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
            # response.set_cookie('throttle', encode(f'1_{now}_{until}'))
            memory.throttle = encode(f'1_{now}_{until}')
            memory.save()
        else:
            current_hit = current_hit + 1
            # response.set_cookie('throttle', encode(f'{current_hit}_{_from}_{until}'))
            memory.throttle = encode(f'{current_hit}_{_from}_{until}')
            memory.save()
        
        return response


class ThrottleCheckerForViewsMiddleware:
    def __init__(self, response): # 0
        self.response = response
    
    def __call__(self, request): # 1
        return self.response(request)
    
    def process_view(self, request, obj, view_args, view_kwargs): # 2
        ip = get_client_ip(request)
        view_name = f'{obj.__module__}.{obj.__name__}'
        
        try:
            view = View.objects.get(name=view_name)
            flag = True
        except:
            flag = False
        
        if flag:
            
            flag = False
            
            hit_number, per, duration = expand_limit(view.limit)
            
            view_memory, created = ViewMemory.objects.get_or_create(ip=ip)
            
            total_duration = per * LIMIT_DURATION[duration] # at all
            
            if created:
                now = epoch()
                until = now + total_duration
                
                view_memory.view = view
                view_memory.throttle = encode(f'1_{now}_{until}')
                view_memory.save()
            else:
                throttle = view_memory.throttle
                flag = True
            
            if flag:
                throttle = throttle[2:-1]
                throttle = bytes(throttle.encode('utf-8'))
                throttle = decode(throttle)
                
                current_hit, _from, until = throttle_split(throttle)
                
                now = epoch()
                if (now < until) and (current_hit >= hit_number):
                    return HttpResponseBadRequest()
                elif now >= until:
                    until = now + total_duration
                    view_memory.throttle = encode(f'1_{now}_{until}')
                    view_memory.save()
                else:
                    current_hit = current_hit + 1
                    view_memory.throttle = encode(f'{current_hit}_{_from}_{until}')
                    view_memory.save()


class ThrottleOpperator:
    pass


limit = None
first = True
def throttle(_limit=None):
    global first
    if first:
        View.objects.all().delete()
    else:
        first = False
    
    global limit
    limit = _limit
    def wrapper(obj):
        # obj is a function view or a class based view
        
        name = f'{obj.__module__}.{obj.__name__}'
        
        global limit
        if limit == None:
            limit = LIMIT
        
        view, created = View.objects.get_or_create(name=name)
        view.limit = limit
        view.save()
        
        view.view_memories.all().delete()
        
        return obj
    return wrapper
