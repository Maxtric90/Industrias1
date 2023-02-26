from django import template
from datetime import date, timedelta
from corrida.models import Corrida

register = template.Library()

@register.simple_tag
def corridaAno():
    corridaData=list(Corrida.objects.all())
    return corridaData[0].ano

@register.simple_tag
def corridaFechaLimite():
    corridaData=list(Corrida.objects.all())
    return corridaData[0].fechaLimite

#Si la fecha actual es mayor a la fecha de corrida
@register.simple_tag
def cambiosAceptados():
    today = date.today()
    corridaData=list(Corrida.objects.all())
    if today < corridaData[0].fechaLimite + timedelta(days=1):
        return True 
    return False