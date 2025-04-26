from django.db import models

class Material(models.Model):
    codigo = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)

    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='materiales')
    proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT, related_name='materiales')
    unidad = models.ForeignKey('Unidad', on_delete=models.PROTECT, related_name='materiales')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"{self.nombre} - ${self.precio_venta}"
