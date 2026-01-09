# Ejemplo 6: Asociación 1 a muchos (Curso -> Estudiante)
class Estudiante:
    def __init__(self, nombre: str):
        self.nombre = nombre

class Modulo:
    def __init__(self, nombre):
        self.nombre = nombre

class Curso:
    def __init__(self, titulo: str):
        self.titulo = titulo
        self.estudiantes: list[Estudiante] = []  # multiplicidad *
        self.modulo : list[Modulo]

    def crear_modulo(self, cantidad: int):
        for c in range(cantidad):
            modulo = Modulo(f"Moludo {c}")
            self.modulo.append(modulo)

    def inscribir(self, estudiante: Estudiante) -> None:
        if len(self.estudiantes) <= 4:
            self.estudiantes.append(estudiante)
            print(f"Alumno {estudiante.nombre} inscrito en el curso de {self.titulo}")
        elif len(self.estudiantes) > 4:
            print(f"El alumno {estudiante.nombre} no fue inscrito en el curso {self.titulo} por maximo de estudiantes")
        else:
            print("Error")

estudiante1 = Estudiante("Marcos")
estudiante2 = Estudiante("Katiuska")
estudiante3 = Estudiante("Patricia")
estudiante4 = Estudiante("Maria elena")
estudiante5 = Estudiante("Miguel")
estudiante6 = Estudiante("Rafael")

python = Curso("Python")
java = Curso("Java")

python.inscribir(estudiante1)
python.inscribir(estudiante2)
python.inscribir(estudiante3)
python.inscribir(estudiante4)
python.inscribir(estudiante5)
python.inscribir(estudiante6)
java.inscribir(estudiante6)

python.crear_modulo(5)