from typing import Any
from django.urls import path
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse


class Controller:
    def __getattribute__(self, __name: str) -> Any:
        print(__name)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print('call')
    
    def __enter__(self):
        print('enter')
    
    def __exit__(self, exc_type, exc_value, trace):
        print('exit')
    
    def check(func):
        def wrapper(*args, **kw):
            res = func(*args, **kw)
            print(func)
            return res
            # pass
        return wrapper
    
    @check
    def index(request):
        return HttpResponse('Index.')




class Route:
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns
    
    def get(self, route, view, name):
        # return HttpResponseNotAllowed(['GET'])
        
        self.urlpatterns.append(
            path(route, view, name=name)
        )
        return self.urlpatterns