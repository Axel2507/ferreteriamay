from django.db import models

class Unidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    abreviacion = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.abreviacion})"
