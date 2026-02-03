# Definición de la clase
class Persona:
    def __init__(self, id: int, nombre: str, apellido: str, edad: int):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

# Crear 3 objetos (exactamente los mismos datos que en SQL)
persona1 = Persona(1, "Juan", "Perez", 30)
persona2 = Persona(2, "Maria", "Gonzalez", 25)
persona3 = Persona(3, "Carlos", "Rojas", 40)

"""
persona
id | nombre | apellido  | edad
1 | Juan   | Perez     | 30
2 | Maria  | Gonzalez  | 25
3 | Carlos | Rojas     | 40
"""
