from .models import Corrida
from django.contrib import admin

class CorridaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Corrida, CorridaAdmin)
