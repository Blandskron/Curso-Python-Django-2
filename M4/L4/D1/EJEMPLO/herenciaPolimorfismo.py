import uuid

class Abuelo:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        # Identidad única del abuelo (para diferenciar 2 "Juan Perez")
        self._id = str(uuid.uuid4())

    def __eq__(self, other):
        if not isinstance(other, Abuelo):
            return NotImplemented
        return self._id == other._id

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


# ====== 2 abuelos con mismo nombre ======
abuelo1 = Abuelo("Juan", "Perez")  # Juan Perez 1 (dueño del terreno)
abuelo2 = Abuelo("Juan", "Perez")  # Juan Perez 2 (otro distinto)

# Descendencia REAL del abuelo1
padre = Padre("Raul", abuelo1.apellido, abuelo1)
padre2 = Padre("Roberto", abuelo1.apellido, abuelo1)

nieto = Nieto("Alejandro", padre.apellido, padre)
nieto2 = Nieto("Daniel", padre2.apellido, padre2)
nieto3 = Nieto("Matias", padre2.apellido, padre2)

# "Impostor": descendiente del abuelo2, pero quiere cobrar del abuelo1
padre_impostor = Padre("Tomas", abuelo2.apellido, abuelo2)
nieto_impostor = Nieto("Ignacio", padre_impostor.apellido, padre_impostor)

personas = [nieto, nieto2, nieto3, nieto_impostor]

for persona in personas:
    print(persona.presentarse())

print("\n--- Validación con == (equal) ---")
print("¿abuelo1 == abuelo2?:", abuelo1 == abuelo2)

# ====== Herencia del terreno: abuelo1 hereda el 20% ======
porcentaje_terreno = 20

# Filtramos solo los nietos que realmente son del abuelo1 usando ==
herederos_validos = [p for p in personas if p.abuelo == abuelo1]

print("\nHerederos válidos del 20% (solo del abuelo1):")
for h in herederos_validos:
    print("-", h.nombre, h.apellido)

# Reparto simple: el 20% se divide en partes iguales entre herederos válidos
if herederos_validos:
    parte = porcentaje_terreno / len(herederos_validos)
else:
    parte = 0

print(f"\nCada heredero válido recibe: {parte:.2f}%")

# Mostrar si el impostor intenta cobrar
print("\n¿El impostor puede cobrar del abuelo1?")
print(nieto_impostor.nombre, "=>", "SÍ" if nieto_impostor.abuelo == abuelo1 else "NO")
