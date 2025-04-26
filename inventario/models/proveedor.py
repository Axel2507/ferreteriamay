from django.db import models

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)
    nombre_contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def desactivar(self):
        """Marca al proveedor como inactivo sin eliminarlo (útil para historial de materiales)"""
        self.activo = False
        self.save()

    def activar(self):
        """Restaura a un proveedor previamente desactivado"""
        self.activo = True
        self.save()