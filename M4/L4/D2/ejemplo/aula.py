clases_grabadas = []

class Grabaciones():
    def __init__(self, nombre):
        self.nombre = nombre

class LeccionSincrona:
    def envivo(self, numero):
        return f"Inicio Clase {numero}"
    
    def grabar_seccion(self, numero):
        grabacion = Grabaciones(numero)
        clases_grabadas.append(grabacion)

    def __del__(self):
        print("Clase Terminada")

class Aula:
    def __init__(self, nombre):
        self.nombre = nombre
        self.leccionSincrona = LeccionSincrona()

    def iniciar(self, numero_leccion):
        self.leccionSincrona.grabar_seccion(numero_leccion)
        return self.leccionSincrona.envivo(numero_leccion)
    
class Profesor:
    def __init__(self, nombre, aula: Aula):
        self.nombre = nombre
        self.aula = aula

    def iniciar_leccion(self, leccion):
        return self.aula.iniciar(leccion)

sustantiva = Aula("Sustantiva")
patricia = Profesor("Patricia", sustantiva)

print(f"Dia uno {patricia.iniciar_leccion("Leccion numero 5 Modulo 8")}")
print(f"Dia dos {patricia.iniciar_leccion("Leccion numero 6 Modulo 8")}")        
print(f"Dia tres {patricia.iniciar_leccion("Leccion numero 7 Modulo 8")}")          
print(clases_grabadas)