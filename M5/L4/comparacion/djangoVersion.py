from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

Persona.objects.create(
    id=1,
    nombre="Juan",
    apellido="Perez",
    edad=30
)

Persona.objects.create(
    id=2,
    nombre="Maria",
    apellido="Gonzalez",
    edad=25
)

Persona.objects.create(
    id=3,
    nombre="Carlos",
    apellido="Rojas",
    edad=40
)

"""
persona
id | nombre | apellido  | edad
1 | Juan   | Perez     | 30
2 | Maria  | Gonzalez  | 25
3 | Carlos | Rojas     | 40
"""