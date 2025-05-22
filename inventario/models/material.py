from django.db import models

class Material(models.Model):
    codigo = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=100, unique=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)

    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='materiales')
    proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT, related_name='materiales')
    unidad_compra = models.ForeignKey('Unidad', on_delete=models.PROTECT, related_name="materiales_compra", default=1)
    unidad_venta = models.ForeignKey('Unidad', on_delete=models.PROTECT, related_name="materiales_venta", default=1)
    factor_conversion = models.PositiveIntegerField(default=1)
    fecha_caducidad = models.DateField(null=True, blank=True)

    activo = models.BooleanField(default=True)
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"{self.nombre} - ${self.precio_venta}"
    
    def desactivar(self):
        """Desactiva esta categoría sin eliminarla"""
        self.activa = False
        self.save()

    def activar(self):
        """Activa esta categoría"""
        self.activa = True
        self.save()