
#
import mimetypes
import posixpath
from pathlib import Path
import re
from urllib.parse import urlsplit

from django.http import (
    FileResponse, Http404, HttpResponseNotModified, HttpResponseForbidden
)
from django.utils._os import safe_join
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views.static import directory_index, was_modified_since
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.contrib.auth import get_user_model

import jwt
from rest_framework_simplejwt.state import api_settings

from app.models import FileAccess

User = get_user_model()


def serve(request, token, document_root=None, show_indexes=False):
    """
    Serve static files below a given point in the directory structure.

    To use, put a URL pattern such as::

        from django.views.static import serve

        path('<path:path>', serve, {'document_root': '/path/to/my/files/'})

    in your URLconf. You must provide the ``document_root`` param. You may
    also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
    of the directory.  This index view will use the template hardcoded below,
    but if you'd like to override it, you can create a template called
    ``static/directory_index.html``.
    """
    
    # /media/<JWT-Token>/
    user = request.user
    token = token.strip('/')
    if '/' in token:
        token = token.split('/')[0]
    #
    access = FileAccess.objects.get(jwt_token=token)
    #
    _token = jwt.decode(
        jwt=token, key=settings.SECRET_KEY,
        algorithms=[api_settings.ALGORITHM]
    )
    path = _token.get('file_path')
    #
    user_id = _token.get('user_id')
    print(user_id)
    if user_id is not None:
        token_user = User.objects.get(id=user_id)
        if user != token_user:
            return HttpResponseForbidden('UnAuthorized.')
    """
    path = posixpath.normpath(path).lstrip('/')
    post_picture = get_object_or_404(PostPicture, picture=path)
    access = get_object_or_404(Access, user=user, post_picture=post_picture)
    #
    public file
    with user access permission
    with superuser access permission
    with permission access
    with group access
    with token, then token to a file
    with temporary-token, then token to a file
    """

    path = posixpath.normpath(path).lstrip('/')
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_dir():
        if show_indexes:
            return directory_index(path, fullpath)
        raise Http404(_("Directory indexes are not allowed here."))
    if not fullpath.exists():
        raise Http404(_('“%(path)s” does not exist') % {'path': fullpath})
    # Respect the If-Modified-Since header.
    statobj = fullpath.stat()
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(str(fullpath))
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(fullpath.open('rb'), content_type=content_type)
    response.headers["Last-Modified"] = http_date(statobj.st_mtime)
    if encoding:
        response.headers["Content-Encoding"] = encoding
    return response






def static(prefix, view=serve, **kwargs):
    """
    Return a URL pattern for serving files in debug mode.

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    """
    elif not settings.DEBUG or urlsplit(prefix).netloc:
        # No-op if not in debug mode or a non-local prefix.
        return []
    """
    return [
        # re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
        re_path(r'^%s(?P<token>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]
