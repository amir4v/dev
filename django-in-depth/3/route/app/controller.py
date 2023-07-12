from typing import Any, Self, Union

from django.urls import path
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed


class Controller:
    urlpatterns = list()
    prefix_route = '' # Must not start with / ; and Must end with / ; Can be empty.
    
    def __init__(self, urlpatterns) -> None:
        self.urlpatterns = urlpatterns

import inspect
def _get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.__self__.__class__):
        if meth.__name__ in cls.__dict__:
            return cls
    return None
def get_class_that_defined_method(meth):
    return meth.__qualname__
def route(path: Union[None, str]=None, http_methods: Union[str, tuple, list]='GET', name: Union[None, str]=None, controller: Union[None, Controller]=None):
    if isinstance(http_methods, str):
        http_methods = (http_methods,)
    # if not controller:
    #     raise Exception('Controller cannot be None!')
    def decorator(view):
        # exec(view.__module__.split('.')[2] + view.__qualname__.split('.')[0])
        # getattr(view.__module__, view.__qualname__)
        print(view.__qualname__, view.__module__)
        # controller.urlpatterns.append(
        #     path(controller.prefix_route+path, view, name=name)
        # )
        def wrapper(request, *args, **kwargs):
            if request.method not in http_methods:
                return HttpResponseNotAllowed(http_methods)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator