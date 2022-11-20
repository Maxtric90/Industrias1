import re
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Demanda, PatrimonioMateriales, Trituradora, CurvaGranulometrica, CurvaGranulometricaMaterial, Patrimonio, Material, Demanda
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def curva(request, id, tipo):
    if tipo =='Trituradora':
        entidad=get_object_or_404(Trituradora, id=id)
        curvas=get_list_or_404(CurvaGranulometrica, trituradora__pk=id)
    else:
        entidad=get_object_or_404(PatrimonioMateriales, id=id)
        curvas=get_list_or_404(CurvaGranulometricaMaterial, material__pk=id)
    
    return render(request, "mercado/curva.html", {'id':id, 'curvas':curvas, 'entidad':entidad, 'tipo': tipo})

def mercadoTrituradoras(request):
    trituradoras=Trituradora.objects.all()

    if request.method=="POST":
        opcionSeleccionada=request.POST.get('trituradora_id')
        trituradoraComprada=get_object_or_404(Trituradora, id=opcionSeleccionada)
        if request.user.dinero >= trituradoraComprada.precio:
            print("paso por aca")
            patrimonio = Patrimonio.objects.create(usuario=request.user, trituradora=trituradoraComprada)
            patrimonio.save()
            usuario=request.user
            usuario.dinero=usuario.dinero-trituradoraComprada.precio
            usuario.save()
        else:
            opcionSeleccionada=None
    else:
        opcionSeleccionada=None

    return render(request, "mercado/trituradoras.html", {'trituradoras':trituradoras, 'opcionSeleccionada':opcionSeleccionada})

def mercado_demanda(request):
    demanda=Demanda.objects.all()

    return render(request, "mercado/mercado_demanda.html", {'demanda':demanda})