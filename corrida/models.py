from django.db import models

# Create your models here.
class Corrida(models.Model):
    ano = models.IntegerField()
    fechaLimite=models.DateField()
    
    class Meta:
        verbose_name ='corrida'
        verbose_name_plural='corridas'

    def __str__(self):
        return "{}: disponible hasta {}".format(self.ano, self.fechaLimite)