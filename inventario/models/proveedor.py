from django.db import models

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=150, unique=True)
    nombre_contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(null=True,unique=True)
    direccion = models.TextField(max_length=55, default='')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_empresa']

    def __str__(self):
        return f"{self.nombre_empresa} - {self.nombre_contacto}"

    def desactivar(self):
        """Marca al proveedor como inactivo sin eliminarlo (útil para historial de materiales)"""
        self.activo = False
        self.save()

    def activar(self):
        """Restaura a un proveedor previamente desactivado"""
        self.activo = True
        self.save()