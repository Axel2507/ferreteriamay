from django.db import models
from inventario.models.material import Material

class Descuento(models.Model):
    id_desc = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de descuento, ej. 15.00")

    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    
    estado = models.BooleanField(default=True, help_text="Indica si el descuento está activo o no")
    
    material = models.ForeignKey(Material, to_field="codigo", on_delete=models.CASCADE, related_name="descuentos")

    class Meta:
        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%) para {self.material.nombre}"