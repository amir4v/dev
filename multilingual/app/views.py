from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


def home(request):
    return render(request, 'home.html', {'text': _('Some random test text!')})


def test(request):
    return HttpResponse(_('Some random test text!'))
