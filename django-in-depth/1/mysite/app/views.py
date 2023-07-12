from pprint import pprint
from typing import Any, Optional

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic import View
from django.views.generic import *

from . import forms
from .models import Post

# post = Post.objects.first()
# form = forms.PostForm(instance=post)


from django.contrib import auth, admin, admindocs, contenttypes, flatpages, gis, \
                           humanize, messages, postgres, redirects, sessions, \
                           sitemaps, sites, staticfiles, syndication
#
###############################################################################
from django.contrib.auth import admin, apps, authenticate, backends, base_user, \
                                checks, context_processors, models, decorators, \
                                forms, get_backends, \
                                get_permission_codename, get_user, get_user_model, \
                                handlers, hashers, load_backend, login, logout, \
                                management, middleware, migrations, mixins, \
                                password_validation, signals, tokens, \
                                update_session_auth_hash, urls, validators, views
                                # default_app_config
#
###############################################################################
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
#
###############################################################################
from django.contrib.contenttypes.models import ContentType
# from django.contrib.sites.models import Site
from django.contrib.admin import AdminSite
# from django.contrib.sites.admin import SiteAdmin
#
###############################################################################
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.admin import register
from django.contrib.admin import display
#
###############################################################################
from django.contrib.auth.forms import AuthenticationForm, AdminPasswordChangeForm, \
                                      PasswordChangeForm, PasswordResetForm, \
                                      SetPasswordForm, UserChangeForm, \
                                      UserCreationForm
#
###############################################################################
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, AnonymousUser, \
                                       User, BaseUserManager, UserManager, Group, \
                                       GroupManager, Permission, PermissionManager, PermissionsMixin
#
###############################################################################
from django.contrib.auth.password_validation import validate_password, get_default_password_validators, get_password_validators
#
###############################################################################
from django.contrib.auth.backends import ModelBackend, AllowAllUsersModelBackend, \
                                         AllowAllUsersRemoteUserBackend, BaseBackend, RemoteUserBackend
from django.contrib.syndication.views import Feed
from django.contrib.admin.models import LogEntry, LogEntryManager
#
###############################################################################
from django.contrib.auth.hashers import make_password, check_password, get_hasher, \
                                        get_hashers, get_hashers_by_algorithm, \
                                        identify_hasher, is_password_usable, \
                                        mask_hash, reset_hashers
#
###############################################################################
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
#
###############################################################################
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, \
                                      PasswordChangeView, PasswordContextMixin, \
                                      PasswordResetCompleteView, PasswordResetConfirmView, \
                                      PasswordResetDoneView, PasswordResetView, SuccessURLAllowedHostsMixin
#
from django.http import HttpResponse, HttpRequest, BadHeaderError, FileResponse, \
                        Http404, HttpResponseBadRequest, HttpResponseForbidden, \
                        HttpResponseGone, HttpResponseNotAllowed, HttpResponseNotFound, \
                        HttpResponseNotModified, HttpResponsePermanentRedirect, \
                        HttpResponseRedirect, HttpResponseServerError, JsonResponse, \
                        QueryDict, RawPostDataException, SimpleCookie, StreamingHttpResponse, UnreadablePostError





# class HomeView(LoginRequiredMixin, View):
# class HomeView(PermissionRequiredMixin, View):
class HomeView(View):
    AccessMixin, LoginRequiredMixin, PermissionRequiredMixin
    
    # permission_required = 'app.set_published_status'
    
    def get(self, request):
        return render(request, 'app/home.html')






class _HomeView(UserPassesTestMixin, View):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
    
    template_name = 'app/home.html'
    
    def test_func(self):
        login(self.request, User.objects.last())
        print(self.request.user.has_perm('app.set_published_status'))
        return self.request.user.has_perm('app.set_published_status')
    
    def get(self, request):
        login(self.request, User.objects.last())
        return render(request, self.template_name)




@permission_required('app.view_post')
@permission_required(['app.view_post', 'app.change_post'])
def _home(request):
    User, Group, Permission
    author_group, created_author_group = Group.objects.get_or_create(name='author')
    editor_group, created_editor_group = Group.objects.get_or_create(name='editor')
    publisher_group, created_publisher_group = Group.objects.get_or_create(name='publisher')
    
    content_type = ContentType.objects.get_for_model(Post)
    post_permissions = Permission.objects.filter(content_type=content_type)
    
    for perm in post_permissions:
        if perm.codename == 'delete_post':
            publisher_group.permissions.add(perm)
        elif perm.codename == 'change_post':
            publisher_group.permissions.add(perm)
            editor_group.permissions.add(perm)
        else:
            publisher_group.permissions.add(perm)
            editor_group.permissions.add(perm)
            author_group.permissions.add(perm)
    
    user, created_user = User.objects.get_or_create(username="test-2")
    user.groups.add(author_group)
    
    user = get_object_or_404(User, pk=user.id)
    print(user.has_perm("app.delete_post")) # => False
    print(user.has_perm("app.change_post")) # => False
    print(user.has_perm("app.view_post")) # => True
    print(user.has_perm("app.add_post")) # => True
    
    """You can also check for permissions in your Django templates. With Django's auth context processors,
    a perms variable is available by default when you render your template.
    The perms variable actually contains all permissions in your Django application.
    For example:
        {% if perms.blog.view_post %}
            {# Your content here #}
        {% endif %}"""
    
    return render(request, 'app/home.html')




def _home(request):
    User, Group, Permission
    """By default, Django will create the following permissions:
        app.add_post
        app.change_post
        app.delete_post
        app.view_post"""
    
    content_type = ContentType.objects.get_for_model(Post)
    post_permissions = Permission.objects.filter(content_type=content_type)
    print([perm.codename for perm in post_permissions])
    
    user = User.objects.get(username='test')
    print(user.has_perm('app.change_post')) # False
    for perm in post_permissions:
        user.user_permissions.add(perm)
    print(user.has_perm('app.change_post'))
    # => False
    # Why? This is because Django's permissions do not take
    # effect until you allocate a new instance of the user.
    user = get_user_model().objects.get(username='test')
    print(user.has_perm("app.view_post"))
    # => True
    
    return render(request, 'app/home.html')





def _home(request):
    AuthenticationForm, AdminPasswordChangeForm, \
    PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm, UserChangeForm, \
    UserCreationForm
    
    the_form = UserCreationForm
    the_form = AuthenticationForm
    the_form = AdminPasswordChangeForm
    the_form = PasswordChangeForm
    the_form = PasswordResetForm
    the_form = SetPasswordForm
    the_form = UserChangeForm
    
    if request.method == 'POST':
        # form = the_form()
        # form = the_form(request, request.POST)
        # form = the_form(request.user, request.POST)
        form = the_form(request.POST)
        if form.is_valid():
            form.save()
            # user = form.user_cache
            # login(request, user)
            return render(request, 'app/home.html')
            # form = the_form(request.user)
    elif request.method == 'GET':
        form = the_form()
    
    # if request.user.is_authenticated:
    #     return render(request, 'app/home.html')
    return render(request, 'app/home.html', {'form': form})





# Create a form to edit an existing Article, but use
# POST data to populate the form.
# a = Article.objects.get(pk=1)
# f = ArticleForm(request.POST, instance=a)
# f.save()





# @login_required()
# @permission_required(['create_post'])
def _home(request):
    auth = authenticate(request, username='admin', password='admin')
    print(auth)
    
    print(get_user(request))
    print(get_user_model())
    
    user = User.objects.first()
    login(request, user)
    logout(request)
    
    middleware.AuthenticationMiddleware
    middleware.RemoteUserMiddleware
    middleware.PersistentRemoteUserMiddleware
    
    password_validation, signals, tokens, update_session_auth_hash, urls, validators, views
    """
    print(
        password_validation.validate_password('admin'),
        password_validation.validate_password('admin', user)
    )
    """
    signals.user_logged_in
    signals.user_login_failed
    signals.user_logged_out
    print(signals.user_logged_in.__dict__)
    #
    pprint(urls.urlpatterns)
    
    login_required, permission_required
    #
    # @login_required()
    # @permission_required(['create_post'])
    
    return StreamingHttpResponse('abc...')
    
    return JsonResponse({'name': 'Amir', 'age': 23})
    
    return HttpResponseServerError('serdver terekeide')
    
    return HttpResponseRedirect('/')
    
    return HttpResponsePermanentRedirect('/')
    
    return HttpResponseNotModified()
    
    return HttpResponseNotFound('notofondo')
    
    return HttpResponseNotAllowed(['GET'])
    
    return HttpResponseGone('gonnnnneeee   2')
    
    return HttpResponseForbidden('yo ho ')
    
    return HttpResponseBadRequest('wassap daowg!')
    
    return FileResponse(open(settings.BASE_DIR/'app/views.py', 'rb'))
    
    # This code defines a view function called `home` that renders a template
    # called `app/home.html`. It creates an instance of a form called `MyForm`
    # using the POST data from the request, and checks if the form is valid. If
    # the form is valid, it prints a message and the cleaned data from the form.
    # Finally, it passes the form to the template context as `form`.
    my_form = forms.MyForm(request.POST)
    if my_form.is_valid():
        print('IS _ VALID')
        print(my_form.cleaned_data)
    return render(request, 'app/home.html', {'form': my_form})