from django.contrib import admin
from .models import RegistroClima

@admin.register(RegistroClima)
class RegistroClimaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'temperatura', 'humedad', 'presion', 'velocidad_viento', 'nubosidad')
    list_filter = ('fecha', 'temperatura', 'humedad')
    search_fields = ('fecha',)
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)
