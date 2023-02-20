from django.http import HttpResponse
from django.shortcuts import render
from Industrias1App.models import CustomUser
from mercado.models import Patrimonio


# Create your views here.
def home(request):
    return render(request, "Industrias1App/home.html")

def home_instrucciones(request):
    return render(request, "Industrias1App/home_instrucciones.html")

def home_ranking(request):
    class TablaRanking:
        def __init__(self, userID, usuario, dinero, valorEquipos):
            self.userID = userID
            self.usuario = usuario
            self.dinero = dinero
            self.valorEquipos = valorEquipos

    usuarios=list(CustomUser.objects.all().order_by('-dinero'))
    patrimonios=list(Patrimonio.objects.all())
    
    tabla=[]
    for usuario in usuarios:
        tabla.append(TablaRanking(usuario.id, usuario, usuario.dinero, 0))

    for registro in tabla:
        for patrimonio in patrimonios:
            if registro.userID == patrimonio.usuario.id:
                registro.valorEquipos = registro.valorEquipos + patrimonio.valorActual

    tabla.sort(key=lambda x: x.dinero + x.valorEquipos, reverse = True)
    return render(request, "Industrias1App/home_ranking.html", {'tabla':tabla})