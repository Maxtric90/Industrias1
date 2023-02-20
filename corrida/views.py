from django.shortcuts import render, get_object_or_404
from Industrias1App.models import CustomUser
from mercado.models import Layout, PatrimonioMateriales, Material, Patrimonio
from corrida.ejecucion import ejecutarLayout, ventaMaterial, agregarMaterialMenu

# Create your views here.
def corrida(request):
    usuarios=list(CustomUser.objects.all())
    layouts=list(Layout.objects.all())
    detalleVenta=None
    infoDinero=None
    mensajes=None
    if request.method=="POST":
        usuarios=CustomUser.objects.all()
        detalleVenta=[]
        infoDinero=[]
        mensajes=[] #Aquí se guardan los mensajes de las corridas
        for usuario in usuarios:
            ganancia=0
            dineroOriginal=usuario.dinero
            #Trituración de materiales
            print("******Inicio ejecución layout usuario ", usuario, " ******")
            if ejecutarLayout(usuario.id)==0:
                print("La ejecución ha sido exitosa")
                print("******Fin de ejecucion layout usuario ", usuario, " ******")
                mensajes.append([usuario.id, "Corrida exitosa"])
            else:
                print("La ejecución no tuvo éxito (por tamaños máximos o caudales)")
                print("******Fin de ejecucion layout usuario ", usuario, " ******")
                mensajes.append([usuario.id, "La corrida no tuvo éxito (por tamaños máximos o caudales)"])
            #Venta de materiales
            print("******Inicio venta materiales usuario ", usuario, " ******")
            registroVenta=ventaMaterial(usuario.id)
            print("******Fin venta materiales usuario ", usuario, " ******")
            detalleVenta=detalleVenta + registroVenta
            for registro in registroVenta:
                ganancia+=registro[6]
            infoDinero.append([usuario.id,dineroOriginal,ganancia,dineroOriginal+ganancia])
            #Amortizaciones de equipos
            print("******Inicio amortización equipos usuario ", usuario, " ******")
            patrimonio=list(Patrimonio.objects.filter(usuario_id=usuario.id))
            for equipo in patrimonio:
                valorActualizado=equipo.valorActual - equipo.trituradora.precio * 0.1
                if valorActualizado < 0:
                    valorActualizado = 0
                print(equipo.trituradora.modelo,':', equipo.valorActual,  '->', valorActualizado)
                Patrimonio.objects.filter(pk=equipo.pk).update(valorActual=valorActualizado)
            print("******Fin amortización equipos usuario ", usuario, " ******")

            

    return render(request, "corrida/corrida.html", {'layouts': layouts,'detalleVenta':detalleVenta, 'usuarios': usuarios,'infoDinero': infoDinero, 'mensajes': mensajes})

def configuracion(request):
    materiales=list(Material.objects.all())
    if request.method=="POST":
        materialInput=get_object_or_404(Material, id=request.POST.get('materialInput'))
        caudalInput=int(request.POST.get('materialCaudal'))
        tamanoInput=int(request.POST.get('materialTamano'))
        agregarMaterialMenu(materialInput, caudalInput, tamanoInput)
    patrimonioMateriales=list(PatrimonioMateriales.objects.all())
    return render(request, "configuracion/configuracion.html", {'patrimonioMateriales': patrimonioMateriales, 'materiales': materiales})