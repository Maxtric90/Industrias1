from django.shortcuts import render
from Industrias1App.models import CustomUser
from mercado.models import Layout
from corrida.ejecucion import ejecutarLayout, ventaMaterial

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
            print("******Inicio ejecución layout usuario ", usuario, " ******")
            if ejecutarLayout(usuario.id)==0:
                print("La ejecución ha sido exitosa")
                print("******Fin de ejecucion layout usuario ", usuario, " ******")
                mensajes.append([usuario.id, "Corrida exitosa"])
            else:
                print("La ejecución no tuvo éxito (por tamaños máximos o caudales)")
                print("******Fin de ejecucion layout usuario ", usuario, " ******")
                mensajes.append([usuario.id, "La corrida no tuvo éxito (por tamaños máximos o caudales)"])
            print("******Inicio venta materiales usuario ", usuario, " ******")
            registroVenta=ventaMaterial(usuario.id)
            print("******Fin venta materiales usuario ", usuario, " ******")
            detalleVenta=detalleVenta + registroVenta
            for registro in registroVenta:
                ganancia+=registro[6]
            infoDinero.append([usuario.id,dineroOriginal,ganancia,dineroOriginal+ganancia])

    return render(request, "corrida/corrida.html", {'layouts': layouts,'detalleVenta':detalleVenta, 'usuarios': usuarios,'infoDinero': infoDinero, 'mensajes': mensajes})