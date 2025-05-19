from django.db import models

class ReporteVentaSemanal(models.Model):
    id_venta = models.IntegerField()
    nombre_material = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    fecha_venta = models.DateField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_material} ({self.cantidad})"
