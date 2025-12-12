from django.contrib import admin
from .models import Turno


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ("numero", "nombre", "estado", "creado")
    list_filter = ("estado",)
    search_fields = ("nombre", "numero")
