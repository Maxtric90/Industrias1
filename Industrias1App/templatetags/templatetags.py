from django import template
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