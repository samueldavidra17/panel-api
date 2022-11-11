from django.contrib import admin
from .models import departamentos_empresas, empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
# Register your models here.

admin.site.register(departamentos_empresas)
admin.site.register(empresas)
admin.site.register(marcas)
admin.site.register(tipos_equipos)
admin.site.register(tipos_equipos_marcas)
admin.site.register(departamentos)
admin.site.register(ubicaciones)
admin.site.register(usuarios)
admin.site.register(informacion)
admin.site.register(modelos)
admin.site.register(equipos)
admin.site.register(impresoras)
admin.site.register(dispositivos)
