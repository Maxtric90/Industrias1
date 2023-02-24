from mercado.models import CurvaGranulometricaMaterial, Demanda, Patrimonio, PatrimonioMateriales, Trituradora, CurvaGranulometrica, Material, Layout
from Industrias1App.models import CustomUser
from django.shortcuts import render, get_object_or_404, get_list_or_404
from datetime import date
import csv

#Esta función devuelve el porcentaje del material de una curva que es menor al tamaño indicado
def menor(tamano, curva):
    tamano_menor=0
    tamano_mayor=0
    porcentaje_menor=0
    for registro in curva:
        if registro.tamano <= tamano:
            tamano_menor=registro.tamano
            porcentaje_menor=registro.porcentaje
        else:
            tamano_mayor=registro.tamano
            porcentaje_mayor=registro.porcentaje
            break

    if tamano_mayor==0: #Si tamano_mayor es 0 significa que no encontró un tamaño mayor al tamaño de entrada en la curva. por ende el 100% de la curva es menor al tamaño indicado
        interpolacion_lineal=100
    else:
        interpolacion_lineal=(porcentaje_mayor-porcentaje_menor)/(tamano_mayor-tamano_menor)*(tamano-tamano_menor)+porcentaje_menor
    return interpolacion_lineal/100
    
def rango(tamanoMinimo, tamanoMaximo, curva):
    porcentajeMinimo=menor(tamanoMinimo, curva)
    porcentajeMaximo=menor(tamanoMaximo, curva)

    return(porcentajeMaximo-porcentajeMinimo)

def tamanoMaximo(curva):
    for registro in curva:
        
        if registro.porcentaje==100:
            return registro.tamano
    return None

#FUNCION TRITURAR
def triturar(trituradora_id, patrimonioMaterial_id):
# Crea Material nuevo con identicas características que material origen
    patrimonioMaterial_resultante=PatrimonioMateriales.objects.get(id=patrimonioMaterial_id)
    trituradora=Trituradora.objects.get(id=trituradora_id)
    curvaTrituradora=list(CurvaGranulometrica.objects.filter(trituradora_id=trituradora_id))
    curvaMaterial=list(CurvaGranulometricaMaterial.objects.filter(material_id=patrimonioMaterial_id))

# Control de que tamaño máximo del material sea menor que abertura de entrada de trituradora
    escrituraArchivo("******Control tamaños******", 'log')
    escrituraArchivo("Tamaño ingreso material: "+ str(tamanoMaximo(curvaMaterial)), 'log')
    escrituraArchivo("Tamaño entrada trituradora: "+ str(trituradora.aberturaEntrada), 'log')
    if tamanoMaximo(curvaMaterial) > float(trituradora.aberturaEntrada):
        escrituraArchivo("Resultado tamaños: ERROR. Se pierde el material", 'log')
        #Se pierde el material
        #patrimonioMaterial_resultante.delete()
        return 1 #Devuelve valor bandera de que el tamaño supera el soportado por la trituradora 
    escrituraArchivo("Resultado tamaños: OK", 'log')

# Control de que el caudal del material sea menor que el material de la trituradora
    escrituraArchivo("******Control caudales******", 'log')
    escrituraArchivo("Caudal ingreso material: " + str(patrimonioMaterial_resultante.caudal) + "tn/h", 'log')
    escrituraArchivo("Dureza: " + str(patrimonioMaterial_resultante.material.dureza), 'log')
    if patrimonioMaterial_resultante.material.dureza=="blando":
        escrituraArchivo("Caudal máximo trituradora: " + str(trituradora.caudalBlando) + "tn/h", 'log')
        if patrimonioMaterial_resultante.caudal > trituradora.caudalBlando:
            escrituraArchivo("Resultado caudales: ERROR. Se pierde el material", 'log')
            #Se pierde el material
            patrimonioMaterial_resultante.delete()
            return 1 #Devuelve valor bandera de que el tamaño supera el soportado por la trituradora            
    if patrimonioMaterial_resultante.material.dureza=="medio":
        escrituraArchivo("Caudal máximo trituradora: " + str(trituradora.caudalMedio) + "tn/h", 'log')
        if patrimonioMaterial_resultante.caudal > trituradora.caudalMedio:
            escrituraArchivo("Resultado caudales: ERROR. Se pierde el material", 'log')
            #Se pierde el material
            patrimonioMaterial_resultante.delete()
            return 1 #Devuelve valor bandera de que el tamaño supera el soportado por la trituradora            
    if patrimonioMaterial_resultante.material.dureza=="duro":
        escrituraArchivo("Caudal máximo trituradora: " + str(trituradora.caudalDuro) + "tn/h", 'log')
        if patrimonioMaterial_resultante.caudal > trituradora.caudalDuro:
            escrituraArchivo("Resultado caudales: ERROR. Se pierde el material", 'log')
            #Se pierde el material
            patrimonioMaterial_resultante.delete()
            return 1 #Devuelve valor bandera de que el tamaño supera el soportado por la trituradora            
    escrituraArchivo("Resultado caudales: OK", 'log')

# Crea curvas para material nueva con idénticos parámetros que curva de trituradora
    #Elimina la curva original
    CurvaGranulometricaMaterial.objects.filter(material_id=patrimonioMaterial_resultante.id).delete()
    # Si el material es más grande que el tamaño máximo de salida de la trituradora -> ejecución normal
    if tamanoMaximo(curvaMaterial) >= tamanoMaximo(curvaTrituradora):
        for registro in curvaTrituradora:
            registro_material=CurvaGranulometricaMaterial(tamano=registro.tamano,porcentaje=registro.porcentaje,material=patrimonioMaterial_resultante)
            registro_material.save()
    # Sino, debe buscar el proporcional:
    else:
        porcentajeMenor = menor(tamanoMaximo(curvaMaterial),curvaTrituradora)
        for registro in curvaTrituradora:
            if registro.tamano <= tamanoMaximo(curvaMaterial):
                registro_material=CurvaGranulometricaMaterial(tamano=registro.tamano,porcentaje=registro.porcentaje/porcentajeMenor,material=patrimonioMaterial_resultante)
                registro_material.save()
    return 0 #Devuelve señal de que la trituración fue correcta

def ejecutarLayout(usuario_id):
    layout=list(Layout.objects.filter(usuario_id=usuario_id))
    if layout == []:
        return 1
    else:
        layout=layout[0]
    escrituraArchivo("******Layout******", 'log')
    escrituraArchivo("Material: " + str(layout.material), 'log')
    escrituraArchivo("Primer Etapa: " + str(layout.primerEtapa), 'log')
    escrituraArchivo("Segunda Etapa: " + str(layout.segundaEtapa), 'log')
    escrituraArchivo("******************", 'log')
    if(layout.primerEtapa != None):
        escrituraArchivo("******Inicio trituración Etapa 1******", 'log')
        if triturar(layout.primerEtapa.trituradora.id,layout.material.id) == 0:
            escrituraArchivo("******Fin trituración Etapa 1******", 'log')
            if(layout.segundaEtapa!=None):
                escrituraArchivo("******Inicio trituración Etapa 2******", 'log')
                return triturar(layout.segundaEtapa.trituradora.id,layout.material.id)
            else:
                return 0
        else:
            escrituraArchivo("******Fin trituración Etapa 1******", 'log')
            return 1

def ventaMaterial(usuario_id):
    patrimonioMateriales=list(PatrimonioMateriales.objects.filter(usuario_id=usuario_id))
    gananciaTotal=0
    jornadaHoras=8 #Esto debería ser una variable de Settings
    jornadas=20 #Esto debería ser una variable de Settings
    detalleVenta=[]
    for activo in patrimonioMateriales:
        curva=list(CurvaGranulometricaMaterial.objects.filter(material_id=activo.id).order_by('tamano'))
        demanda=list(Demanda.objects.filter(material_id=activo.material.id))
        escrituraArchivo("Para el material " +  str(activo.id) + "(" + str(activo.material.nombre) +") con caudal " + str(activo.caudal), 'log')
        for registro in curva:
            escrituraArchivo("Tamano: " + str(registro.tamano)+ " :"+ str(registro.porcentaje), 'log')
        for escala in demanda:
                escrituraArchivo("El porcentaje entre " +str(escala.tamanoDesde)+ " y "+ str(escala.tamanoHasta)+ " es " + str(rango(escala.tamanoDesde, escala.tamanoHasta,curva)*100)+ "%.", 'log')
                caudal_escala=round(activo.caudal*rango(escala.tamanoDesde, escala.tamanoHasta,curva)*jornadas*jornadaHoras,2)
                ganancia=caudal_escala*escala.precio
                escrituraArchivo("La ganacia es $" + str(ganancia), 'log')
                gananciaTotal+=ganancia
                detalleVenta.append([usuario_id, activo.material.nombre,escala.tamanoDesde,escala.tamanoHasta,caudal_escala,escala.precio,round(ganancia)])
        #Eliminar material de Patrimonio del usuario porque ya se consumió
        activo.delete()
    #Incorporamos la ganancia en el usuario
    usuario=CustomUser.objects.get(id=usuario_id)
    usuario.dinero+= gananciaTotal
    usuario.save()

    return detalleVenta
    
def lecturaTrituradoras():
    trituradoras=[]
    curvas=[]
    with open('Trituradoras.csv', newline='') as csvfile:
        with open('curvasTrituradoras.csv', newline='') as csvfile2:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            spamreader2 = csv.reader(csvfile2, delimiter=';', quotechar='|')
            print("********Inicio agregado de trituradoras********")
            #Guardamos las curvas en una lista
            for registro in spamreader2:
                curvas.append([registro[0], registro[1], registro[2]])
            for row in spamreader:
                print(row)
                trituradora=Trituradora(tipo=row[1], modelo=row[2], manto=row[3], aberturaEntrada=row[4], aberturaCierre=row[5], caudalBlando=row[6], caudalMedio=row[7], caudalDuro=row[8], precio=row[9])
                trituradora.save()
                print("********Inicio agregado de curvas********")
                for registro in curvas:
                    if registro[0]==row[0]:
                        curva=CurvaGranulometrica(tamano=registro[1],porcentaje=int(registro[2]), trituradora=trituradora)
                        curva.save()
                        print(registro)
                print("********Fin agregado de curvas********")
                
    print("********Fin agregado de trituradoras********")

#Esta función es para agregar materiales a los usuarios manualmente pero ya se realiza desde menú
def AgregarMaterial():
    usuarios=CustomUser.objects.all()
    materiales=Material.objects.all()
    caudal=20
    tamano=15
    for usuario in usuarios:
        for material in materiales:
            patrimonioMaterial=PatrimonioMateriales(usuario=usuario, material=material, caudal=caudal)
            patrimonioMaterial.save()
            curvaMaterialMax=CurvaGranulometricaMaterial(tamano=tamano, porcentaje=100, material=patrimonioMaterial)
            curvaMaterialAux=CurvaGranulometricaMaterial(tamano=tamano-0.01, porcentaje=0.1, material=patrimonioMaterial)
            curvaMaterialMax.save()
            curvaMaterialAux.save()
            if list(Layout.objects.filter(usuario_id=usuario.id)) ==[]:
                layout=Layout(usuario=usuario, material=patrimonioMaterial)
                layout.save()
            else:
                Layout.objects.filter(usuario_id=usuario.id).update(material=patrimonioMaterial)

def agregarMaterialMenu(material, caudal, tamano):
    usuarios=CustomUser.objects.all()
    for usuario in usuarios:
        patrimonioMaterial=PatrimonioMateriales(usuario=usuario, material=material, caudal=caudal)
        patrimonioMaterial.save()
        curvaMaterialMax=CurvaGranulometricaMaterial(tamano=tamano, porcentaje=100, material=patrimonioMaterial)
        curvaMaterialAux=CurvaGranulometricaMaterial(tamano=tamano-0.01, porcentaje=0.1, material=patrimonioMaterial)
        curvaMaterialMax.save()
        curvaMaterialAux.save()
        if list(Layout.objects.filter(usuario_id=usuario.id)) ==[]:
            layout=Layout(usuario=usuario, material=patrimonioMaterial)
            layout.save()
        else:
            Layout.objects.filter(usuario_id=usuario.id).update(material=patrimonioMaterial)

def escrituraArchivo(texto, tipo):
    today = date.today()
    rutaArchivo= 'corrida/logs/'+ tipo + str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + '.txt'
    with open(rutaArchivo, 'a') as f:
        print(texto)
        f.write(texto)
        f.write('\n')