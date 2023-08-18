from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from common.views import IndexView

urlpatterns = [
    path('enter_admin/', admin.site.urls, name='enter_admin'),
    path('', IndexView.as_view(), name='index'),
    path('users/', include('users.urls', namespace='users')),
    path('files/', include('code_files.urls', namespace='code_files')),
]

urlpatterns.extend(
    [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ],
)
