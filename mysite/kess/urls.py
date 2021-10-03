from django.urls import path

from . import views

app_name = 'kess'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_kess/', views.add_kess, name='add_kess'),
    path('<int:kess_id>/', views.detail, name='detail'),
]
