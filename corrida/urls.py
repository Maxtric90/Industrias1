from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.corrida, name="Corrida"),
    path('configuracion/', views.configuracion, name="Configuracion"),
]
