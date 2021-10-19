from django.urls import include, path, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'kess'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_kess/', views.add_kess, name='add_kess'),
    path('<int:kess_id>/', views.detail, name='detail'),
    re_path(r"^auth/", include("kess.auth")),
    path('signup/', views.signup, name='signup'),
    path('classement/', views.classement, name='classement'),
    path('user/', views.user, name='user'),
    path('user/<str:user_name>/', views.userPublic, name='userPublic'),
    path('allKess/', views.allKess, name='allKess'),
    path('commu/', views.commu, name='commu'),
]