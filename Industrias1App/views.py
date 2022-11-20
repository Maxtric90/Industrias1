from django.http import HttpResponse
from django.shortcuts import render
from Industrias1App.models import CustomUser


# Create your views here.
def home(request):
    return render(request, "Industrias1App/home.html")

def home_instrucciones(request):
    return render(request, "Industrias1App/home_instrucciones.html")

def home_ranking(request):
    usuarios=list(CustomUser.objects.all().order_by('-dinero'))
    return render(request, "Industrias1App/home_ranking.html", {'usuarios':usuarios})