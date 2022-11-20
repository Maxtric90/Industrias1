from django.urls import re_path, path
from Industrias1App import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('home/instrucciones', views.home_instrucciones, name="Home_instrucciones"),
    path('home/ranking', views.home_ranking, name="Home_ranking"),
]
