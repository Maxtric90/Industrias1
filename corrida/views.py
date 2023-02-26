from django.shortcuts import render, get_object_or_404
from Industrias1App.models import CustomUser
from mercado.models import Layout, PatrimonioMateriales, Material, Patrimonio
from corrida.ejecucion import ejecutarLayout, ventaMaterial, agregarMaterialMenu, escrituraArchivo, adelantaCorrida

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
            escrituraArchivo("****************************************************************************",'log')
            escrituraArchivo("******Inicio ejecución layout usuario " + str(usuario) + " ******", 'log')
            if ejecutarLayout(usuario.id)==0:
                escrituraArchivo("La ejecución ha sido exitosa", 'log')
                escrituraArchivo("******Fin de ejecucion layout usuario " + str(usuario) + " ******", 'log')
                mensajes.append([usuario.id, "Corrida exitosa"])
            else:
                escrituraArchivo("La ejecución no tuvo éxito (por tamaños máximos o caudales)", 'log')
                escrituraArchivo("******Fin de ejecucion layout usuario "+ str(usuario) + " ******", 'log')
                mensajes.append([usuario.id, "La corrida no tuvo éxito (por tamaños máximos o caudales)"])
            #Venta de materiales
            escrituraArchivo("******Inicio venta materiales usuario "+ str(usuario) + " ******", 'log')
            registroVenta=ventaMaterial(usuario.id)
            escrituraArchivo("******Fin venta materiales usuario " + str(usuario) + " ******", 'log')
            detalleVenta=detalleVenta + registroVenta
            for registro in registroVenta:
                ganancia+=registro[6]
            infoDinero.append([usuario.id,dineroOriginal,ganancia,dineroOriginal+ganancia])
            #Amortizaciones de equipos
            escrituraArchivo("******Inicio amortización equipos usuario " + str(usuario) + " ******", 'log')
            patrimonio=list(Patrimonio.objects.filter(usuario_id=usuario.id))
            for equipo in patrimonio:
                valorActualizado=equipo.valorActual - equipo.trituradora.precio * 0.1
                if valorActualizado < 0:
                    valorActualizado = 0
                escrituraArchivo(str(equipo.trituradora.modelo) + ':' + str(equipo.valorActual) + '->' + str(valorActualizado), 'log')
                Patrimonio.objects.filter(pk=equipo.pk).update(valorActual=valorActualizado)
            escrituraArchivo("******Fin amortización equipos usuario " + str(usuario) + " ******", 'log')
        #Actualiza los valores de la corrida
        adelantaCorrida()

            

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