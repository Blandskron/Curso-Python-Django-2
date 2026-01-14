clases_grabadas = []

class Grabaciones:
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Grabaciones(nombre={self.nombre!r})"


class LeccionSincrona:
    def envivo(self, numero):
        return f"Inicio Clase {numero}"

    def grabar_seccion(self, numero):
        grabacion = Grabaciones(numero)
        clases_grabadas.append(grabacion)
        return grabacion  # útil para que Aula pueda devolver algo

    def __del__(self):
        print("Clase Terminada")


class Aula:
    def __init__(self, nombre):
        self.nombre = nombre
        self.leccionSincrona = LeccionSincrona()

    def iniciar(self, numero_leccion):
        return self.leccionSincrona.envivo(numero_leccion)

    def iniciar_grabacion(self, numero_leccion):
        return self.leccionSincrona.grabar_seccion(numero_leccion)


class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido


class Profesor(Persona):
    def __init__(self, nombre, apellido, aula: Aula):
        super().__init__(nombre, apellido)
        self.aula = aula

    def iniciar_leccion(self, leccion):
        return self.aula.iniciar(leccion)

    def grabar_leccion(self, leccion):
        return self.aula.iniciar_grabacion(leccion)


sustantiva = Aula("Sustantiva")
patricia = Profesor("Patricia", "Pérez", sustantiva)

print(f"Dia uno {patricia.iniciar_leccion('Leccion numero 5 Modulo 8')}")
print(f"Dia dos {patricia.iniciar_leccion('Leccion numero 6 Modulo 8')}")
print(f"Dia tres {patricia.iniciar_leccion('Leccion numero 7 Modulo 8')}")

# Ejemplo de grabaciones (opcional)
patricia.grabar_leccion("Leccion numero 5 Modulo 8")
patricia.grabar_leccion("Leccion numero 6 Modulo 8")

print(clases_grabadas)
