from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.
# from throttle.middleware import throttle, ThrottleOpperator
from throttle.models import action_throttle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


def index(request):
    action_throttle(user=request.user, limit='ok', raise_exception=True)
    return HttpResponse('OK!')
