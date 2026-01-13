class Abuelo:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def presentarse(self):
        return f"Soy el abuelo {self.nombre} {self.apellido}"


class Padre(Abuelo):
    def __init__(self, nombre, apellido, abuelo):
        super().__init__(abuelo.nombre, abuelo.apellido)
        self.nombre = nombre
        self.abuelo = abuelo

    def presentarse(self):
        return f"Soy {self.nombre} el hijo de {self.abuelo.nombre} {self.abuelo.apellido}"


class Nieto(Padre):
    def __init__(self, nombre, apellido, padre):
        super().__init__(padre.nombre, padre.apellido, padre.abuelo)
        self.nombre = nombre
        self.padre = padre

    def presentarse(self):
        return (
            f"Yo soy {self.nombre} {self.apellido} Nieto de {self.abuelo.nombre} {self.abuelo.apellido} "
            f"Por desendencia de {self.padre.nombre} {self.padre.apellido} "
        )

abuelo = Abuelo("Juan", "Perez")
padre = Padre("Raul", abuelo.apellido, abuelo)
padre2 = Padre("Roberto", abuelo.apellido, abuelo)
nieto = Nieto("Alejandro", padre.apellido, padre)
nieto2 = Nieto("Daniel", padre2.apellido, padre2)
nieto3 = Nieto("Matias", padre2.apellido, padre2)

personas = [nieto, nieto2, nieto3]

for persona in personas:
    print(persona.presentarse())
