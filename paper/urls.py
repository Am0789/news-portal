from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('protect.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('News/', include('News.urls')),
    path('/1stpage/', include('News.urls')),
    path('/2stpage/', include('News.urls')),
    path('accounts/', include('allauth.urls')),
]