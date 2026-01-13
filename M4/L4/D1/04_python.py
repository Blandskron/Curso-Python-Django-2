# Ejemplo 3: Herencia jerárquica

class Animal:
    def sonido(self) -> str:
        return "Sonido genérico"


class Perro(Animal):
    def sonido(self) -> str:
        return "Guau"


class Gato(Animal):
    def sonido(self) -> str:
        return "Miau"
    
class Instrumento():
    def sonido(self):
        return "Sonar"

class Flauta(Instrumento):
    def sonido(self):
        return "Melodia"

# Ejemplo 4: Polimorfismo con una función genérica

def hacer_sonar(sonido) -> None:
    print(sonido.sonido())


elementos: list[Animal, Instrumento] = [Perro(), Gato(), Animal(), Instrumento(), Flauta()]
for a in elementos:
    hacer_sonar(a)
