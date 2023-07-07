from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('protect.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('News/', include('News.urls')),
    path('/main/', include('News.urls')),
    path('accounts/', include('allauth.urls')),
]
