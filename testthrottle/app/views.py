from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.
from throttle.middleware import throttle, ThrottleOpperator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


@throttle('1/3s')
class Index(View):
    def get(self, request):
        return HttpResponse('Index.get   Hi')


@throttle()
def test1(request):
    return HttpResponse('test1')

@throttle('1/10s')
def test2(request):
    return HttpResponse('test2')

@throttle('1/1min')
def test3(request):
    return HttpResponse('test3')

@throttle('1/3s')
def test4(request):
    return HttpResponse('test4')

class testapi(APIView):
    def get(self, request, format=None):
        return Response(status=status.HTTP_202_ACCEPTED)


@throttle('1/3s')
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        
        flag = ThrottleOpperator(op='combine-first-name-and-last-name', limit='1/3s')
        extra = ''
        if flag:
            extra += 'Wooooow'
        
        usernames = [user for user in ('sddsd', 123312, 34.34, 'dfssfd')]
        return HttpResponse(str(usernames)+extra)
