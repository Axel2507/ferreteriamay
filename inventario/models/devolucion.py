from django.db import models
from django.utils import timezone

class Devolucion(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey("inventario.Venta", on_delete=models.CASCADE, related_name="devoluciones")
    motivo = models.TextField()
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, default='pendiente')  # pendiente, procesada, cancelada

    class Meta:
        verbose_name = "Devolución"
        verbose_name_plural = "Devoluciones"

    def __str__(self):
        return f"Devolución #{self.id} - Venta {self.venta.id}"


class DetalleDevolucion(models.Model):
    id = models.AutoField(primary_key=True)
    devolucion = models.ForeignKey("inventario.Devolucion", on_delete=models.CASCADE, related_name="detalles")
    detalle_venta = models.ForeignKey("inventario.DetalleVenta", on_delete=models.CASCADE)
    cantidad_devuelta = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Detalle de devolución"
        verbose_name_plural = "Detalles de devolución"
        unique_together = ('devolucion', 'detalle_venta')

    def __str__(self):
        return f"Devuelto: {self.cantidad_devuelta} de {self.detalle_venta.material.nombre} (Devolución #{self.devolucion.id})"

