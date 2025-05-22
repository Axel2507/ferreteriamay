from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    abreviacion = models.CharField(max_length=3, unique=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.abreviacion})"

    def desactivar(self):
        """Desactiva esta categoría sin eliminarla"""
        self.activa = False
        self.save()

    def activar(self):
        """Activa esta categoría"""
        self.activa = True
        self.save()