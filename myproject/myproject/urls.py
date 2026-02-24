from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

urlpatterns = [
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('catalog/', include('catalog.urls')),
path('contact/', include('contact.urls')),
]