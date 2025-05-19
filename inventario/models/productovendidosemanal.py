from django.db import models

class ProductoVendidoSemanal(models.Model):
    TIPO_CHOICES = [
        ('más vendido', 'Más Vendido'),
        ('menos vendido', 'Menos Vendido'),
    ]

    nombre_material = models.CharField(max_length=100)
    total_vendido = models.IntegerField()
    tipo = models.CharField(max_length=13, choices=TIPO_CHOICES)
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_material} - {self.tipo}"