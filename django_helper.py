from pprint import pprint, pp
from pathlib import Path
from uuid import uuid4
import random
import string
import sys
import os
import re

from django.http import HttpResponse, HttpResponse as response, \
                        HttpRequest, \
                        FileResponse, FileResponse as fresponse, FileResponse as file_response, \
                        Http404, \
                        HttpResponseBadRequest, HttpResponseBadRequest as bad_request, \
                        HttpResponseForbidden, HttpResponseForbidden as forbidden, \
                        HttpResponseNotAllowed, HttpResponseNotAllowed as not_allowed, \
                        HttpResponseNotFound , HttpResponseNotFound as not_found, \
                        JsonResponse, JsonResponse as jresponse, JsonResponse as json_response
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, resolve_url
from django.urls import reverse, reverse_lazy, resolve, path, re_path, include
from django.views.generic import View, CreateView, DetailView, DeleteView, ListView, FormView, RedirectView, TemplateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail

User = get_user_model()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
