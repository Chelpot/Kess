from django.urls import path

from . import views

app_name = 'kess'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:kess_id>/', views.detail, name='detail'),
]
