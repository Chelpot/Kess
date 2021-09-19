from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('kess/', include('kess.urls')),
    path('admin/', admin.site.urls),
]
