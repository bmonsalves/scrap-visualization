from django.urls import path

from . import views

urlpatterns = [
    path('', views.enterprises, name='index'),
    path('start_scrap/', views.start_scrap, name='start')
]
