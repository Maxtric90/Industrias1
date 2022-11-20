from django.urls import re_path, path
from . import views

urlpatterns = [
    #path('', views.mercado, name="Mercado"),
    path('curva/<int:id>/<str:tipo>/', views.curva, name="Curva"),
    path('demanda/', views.mercado_demanda, name="Mercado_demanda"),
    path('', views.mercadoTrituradoras, name="MercadoTrituradoras"),
]
