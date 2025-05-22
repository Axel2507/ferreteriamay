from django.db import models

class Notificacion(models.Model):
    mensaje = models.TextField()
    fecha = models.DateTimeField()
    codigo_material = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-fecha']