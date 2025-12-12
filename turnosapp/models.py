from django.db import models


class Turno(models.Model):
    ESTADOS = [
        ("EN_ESPERA", "En espera"),
        ("LLAMADO", "Llamado"),
        ("ATENDIDO", "Atendido"),
    ]

    numero = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="EN_ESPERA")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Turno #{self.numero} - {self.nombre}"
