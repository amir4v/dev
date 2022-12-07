from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.
from throttle.middleware import throttle_decorator

@throttle_decorator('1/2s')
class Index(View):
    def get(self, request):
        return HttpResponse('Index.get   Hi')
