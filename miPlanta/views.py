from django.shortcuts import render, get_object_or_404, get_list_or_404
from mercado.models import Patrimonio, PatrimonioMateriales, Trituradora, CurvaGranulometrica, Material, Layout

# Create your views here.
def misEquipos(request):
    mensaje = ''
    if request.method=="POST":
        if request.user.is_authenticated:
            currentUser=request.user
            opcionSeleccionada=request.POST.get('equipo_id')
            #Obtiene datos del layout
            layoutUsuario=get_object_or_404(Layout, usuario__pk=currentUser.id)
            primerEtapaId=None
            segundaEtapaId=None
            if layoutUsuario.primerEtapa != None:
                primerEtapaId = layoutUsuario.primerEtapa.id
            if layoutUsuario.segundaEtapa != None:
                segundaEtapaId = layoutUsuario.segundaEtapa.id  
            #Si está intentando vender una trituradora que está configurada en el layout cancela
            if str(primerEtapaId) == str(opcionSeleccionada) or str(segundaEtapaId) == str(opcionSeleccionada):
                opcionSeleccionada=None
                mensaje='No puede vender una trituradora que está siendo utilizada en el Layout. Primero debe quitarla para luego venderla.'
            else:
                trituradoraVendida=get_object_or_404(Patrimonio, id=opcionSeleccionada)
                currentUser.dinero=currentUser.dinero+trituradoraVendida.valorActual
                currentUser.save()
                trituradoraVendida.delete()
        else:
            opcionSeleccionada=None
    else:
        opcionSeleccionada=None

    if request.user.is_authenticated:
        currentUser=request.user
        patrimonio=list(Patrimonio.objects.filter(usuario_id=currentUser.id))
        #patrimonio=get_list_or_404(Patrimonio, usuario_id=currentUser.id)
        if not patrimonio:
            patrimonio=None
    else:
        patrimonio=None

    return render(request, "miPlanta/misEquipos.html", {'patrimonio': patrimonio, 'mensaje': mensaje})

def layout(request):
    if request.user.is_authenticated:
        currentUser=request.user
        mensaje=None
        if request.method=="POST":
            
            if request.POST.get('materialInput') == None:
                mensaje='Debe seleccionar un material'
            else:
                materialInput=get_object_or_404(PatrimonioMateriales, id=request.POST.get('materialInput'))
                if request.POST.get('primerEtapaInput')!='0':
                    primerEtapaInput=get_object_or_404(Patrimonio, id=request.POST.get('primerEtapaInput'))
                else:
                    primerEtapaInput=None
                if request.POST.get('segundaEtapaInput')!='0':
                    segundaEtapaInput=get_object_or_404(Patrimonio, id=request.POST.get('segundaEtapaInput'))
                else:
                    segundaEtapaInput=None    
                
                #Control de que no se usa dos veces la misma trituradora
                if primerEtapaInput == segundaEtapaInput and primerEtapaInput != None:
                    mensaje='No puede utilizar la misma trituradora en dos etapas.'
                else:
                    #Control de que no haya primera etapa y si haya segunda etapa
                    if primerEtapaInput == None and segundaEtapaInput != None:
                        mensaje='No se puede colocar segunda etapa de trituración sin primera etapa de trituración'
                    else:
                        if list(Layout.objects.filter(usuario_id=currentUser.id)):
                            Layout.objects.filter(usuario_id=currentUser.id).update(material=materialInput, primerEtapa=primerEtapaInput, segundaEtapa=segundaEtapaInput)
                        else:
                            layoutAAgregar=Layout(usuario_id=currentUser.id, material=materialInput, primerEtapa=primerEtapaInput, segundaEtapa=segundaEtapaInput)
                            layoutAAgregar.save()
                        mensaje='Layout actualizado con éxito!'

        if list(Layout.objects.filter(usuario_id=currentUser.id))==[]:                 
            layout=None
        else:
            layout=list(Layout.objects.filter(usuario_id=currentUser.id))[0]
        materiales=list(PatrimonioMateriales.objects.filter(usuario_id=currentUser.id))
        trituradoras=list(Patrimonio.objects.filter(usuario_id=currentUser.id))
        if not layout:
            layout=None
    else:
        layout=None
        materiales=None
        trituradoras=None
        mensaje=None

    return render(request, "miPlanta/layout.html", {'layout': layout,'materiales': materiales, 'trituradoras': trituradoras, 'mensaje':mensaje})

def materiales(request):
    if request.user.is_authenticated:
        currentUser=request.user
        materiales=list(PatrimonioMateriales.objects.filter(usuario_id=currentUser.id))
        if not materiales:
            materiales=None
    else:
        materiales=None
    return render(request, "miPlanta/materiales.html", {'materiales': materiales})