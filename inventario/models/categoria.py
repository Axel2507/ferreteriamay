from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)  # Útil para categorías obsoletas

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def desactivar(self):
        """Desactiva esta categoría sin eliminarla (optimización para datos históricos)"""
        self.activa = False
        self.save()

    def activar(self):
        """Restaura esta categoría"""
        self.activa = True
        self.save()