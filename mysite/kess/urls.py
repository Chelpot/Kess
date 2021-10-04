from django.urls import include, path, re_path

from . import views

app_name = 'kess'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_kess/', views.add_kess, name='add_kess'),
    path('<int:kess_id>/', views.detail, name='detail'),
    re_path(r"^auth/", include("kess.auth")),
]
