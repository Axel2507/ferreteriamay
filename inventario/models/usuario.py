from django.db import models

class Usuario(models.Model):
    ROL_CHOICES = [
        ('gerente', 'Gerente'),
        ('empleado', 'Empleado'),
    ]

    usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=8, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.usuario} ({self.rol})"