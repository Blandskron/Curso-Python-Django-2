from django.db import models

class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.calle}, {self.ciudad}"


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.OneToOneField(
        Direccion,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.nombre

"""
TABLA DIRECCION
-------------------------------------
CALLE                   | CIUDAD
-------------------------------------
EVERGREEN TERRACE 742   | SPRINGFIELD
SIEMPRE VIVA 123        | SPRINGFIELD
"""