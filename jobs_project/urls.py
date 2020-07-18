from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancies.urls')),

    re_path(r'^media/(?P<path>.*)$', serve,
            kwargs=dict(document_root=settings.MEDIA_ROOT)),
]
