from .models import CurvaGranulometrica, Patrimonio, Trituradora, Material, CurvaGranulometricaMaterial, PatrimonioMateriales, Demanda, Layout
from django.contrib import admin

# Register your models here.
admin.site.register([CurvaGranulometrica, CurvaGranulometricaMaterial, Trituradora, Patrimonio, Material, PatrimonioMateriales, Demanda, Layout])
