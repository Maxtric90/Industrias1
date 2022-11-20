from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.misEquipos, name="MisEquipos"),
    path('layout', views.layout, name="Layout"),
    path('materiales', views.materiales, name="Materiales"),
]
