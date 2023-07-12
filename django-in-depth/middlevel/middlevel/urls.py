from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'), name='app'),
    # path('accounts/', include('accounts.urls'), name='accounts'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    # path('auth/webauthn/', include('djoser.webauthn.urls')), # not working
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static as default_static
    urlpatterns.extend(
        default_static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )
    )

if not settings.DEBUG:
    from app.static import static
    urlpatterns.extend(
        static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
    )
