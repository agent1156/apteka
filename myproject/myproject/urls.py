from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('catalog/', include('catalog.urls')),
    path('contact/', include('contact.urls')),
    path('news/', include('news.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
