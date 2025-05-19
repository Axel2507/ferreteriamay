from django.db import models

class Notificacion(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField()

    def __str__(self):
        return self.mensaje