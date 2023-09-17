
from django.contrib import admin
from django.urls import path, include

handler404 = 'mainwebsite.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('mainwebsite.urls'))
]
