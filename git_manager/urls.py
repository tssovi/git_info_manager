from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
media_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
root_url = static_url + media_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('git_core.urls')),
] + root_url
