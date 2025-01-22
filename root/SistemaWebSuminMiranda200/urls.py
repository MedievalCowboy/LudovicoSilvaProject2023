
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found, server_error


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('mainwebsite.urls')),

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'mainwebsite.views.custom_404'
