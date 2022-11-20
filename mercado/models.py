from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from Industrias1App.models import CustomUser

# Create your models here.
class Trituradora(models.Model):
    TIPO_TRITURADORA_CHOICES={('conica', 'Conica'), ('mandíbula', 'Mandibulas')}
    MANTO_CHOICES={('medium', 'Medium'), ('course', 'Course'), ('extra-course', 'Extra-Course'), ('ninguno', 'Ninguno')}
    tipo=models.CharField(max_length=20, choices=TIPO_TRITURADORA_CHOICES)
    modelo=models.CharField(max_length=50)
    manto=models.CharField(max_length=20, choices=MANTO_CHOICES)
    aberturaEntrada=models.CharField(max_length=50)
    aberturaCierre=models.CharField(max_length=50)
    caudalBlando=models.FloatField()
    caudalMedio=models.FloatField()
    caudalDuro=models.FloatField()
    precio=models.FloatField()
    imagen=models.ImageField(upload_to='trituradoras', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('mercado:Curva', args=[self.id, "Trituradora"])

    class Meta:
        verbose_name ='trituradora'
        verbose_name_plural='trituradoras'
    
    def __str__(self):
        return "{}- @{}\"".format(self.modelo, self.aberturaCierre)

class Material(models.Model):
    MATERIAL_DUREZA_CHOICES={('blando', 'Blando'), ('medio', 'Medio'), ('duro', 'Duro')}
    nombre= models.CharField(max_length=20)
    dureza=models.CharField(max_length=20, choices=MATERIAL_DUREZA_CHOICES)
#    caudal=models.FloatField() #se quita el caudal de la base de materiales y se incluye en la base de patrimonio
    imagen=models.ImageField(upload_to='materiales', null=True, blank=True)

    class Meta:
        verbose_name ='material'
        verbose_name_plural='Materiales'
    
    def __str__(self):
        return "{} - Dureza: {} ".format(self.nombre, self.dureza)


class CurvaGranulometrica(models.Model):
    tamano=models.FloatField()
    porcentaje=models.FloatField()
    trituradora=models.ForeignKey(Trituradora, on_delete=models.CASCADE)

    class Meta:
        verbose_name ='curva'
        verbose_name_plural='curvas'
    
    def __str__(self):
        return "{} - {} {} %".format(self.trituradora, self.tamano, self.porcentaje)

class PatrimonioMateriales(models.Model):
    usuario=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    material=models.ForeignKey(Material, on_delete=models.CASCADE)
    caudal=models.FloatField()

    def get_absolute_url(self):
        return reverse('mercado:Curva', args=[self.id, 'Material'])

    def __str__(self):
        return "{} - {} ".format(self.usuario.username, self.material, self.caudal)

class CurvaGranulometricaMaterial(models.Model):
    tamano=models.FloatField()
    porcentaje=models.FloatField()
    material=models.ForeignKey(PatrimonioMateriales, on_delete=models.CASCADE)

    class Meta:
        verbose_name ='curva material'
        verbose_name_plural='curvas material'
    
    def __str__(self):
        return "{} - {}\" {} %".format(self.material, self.tamano, self.porcentaje)

class Patrimonio(models.Model):
    usuario=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trituradora=models.ForeignKey(Trituradora, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - Manto; {}".format(self.usuario.username, self.trituradora, self.trituradora.manto)

class Demanda(models.Model):
    material=models.ForeignKey(Material, on_delete=models.CASCADE)
    tamanoDesde=models.FloatField()
    tamanoHasta=models.FloatField()
    precio=models.FloatField()
    
    class Meta:
        verbose_name ='demanda'
        verbose_name_plural='demanda'

    def __str__(self):
        return "{}: desde {}\" hasta {}\"".format(self.material, self.tamanoDesde, self.tamanoHasta)

class Layout(models.Model):
    usuario=models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    material=models.ForeignKey(PatrimonioMateriales, on_delete=models.CASCADE)
    primerEtapa=models.ForeignKey(Patrimonio, on_delete=models.CASCADE, null=True, blank=True, related_name='primerEtapa')
    segundaEtapa=models.ForeignKey(Patrimonio, on_delete=models.CASCADE,null=True, blank=True, related_name='segundaEtapa')

    def __str__(self):
        return "{}-> Material: {}".format(self.usuario.username, self.material.material.nombre)