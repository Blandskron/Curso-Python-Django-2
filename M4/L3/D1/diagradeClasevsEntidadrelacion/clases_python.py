class Direccion:
    def __init__(self, calle: str, ciudad: str):
        self.calle = calle
        self.ciudad = ciudad

class Cliente:
    def __init__(self, nombre: str, direccion: Direccion):
        self.nombre = nombre
        self.direccion = direccion 

"""
TABLA DIRECCION
-------------------------------------
CALLE                   | CIUDAD
-------------------------------------
EVERGREEN TERRACE 742   | SPRINGFIELD
SIEMPRE VIVA 123        | SPRINGFIELD
"""
micasa = Direccion("EVERGREEN TERRACE 742", "SPRINGFIELD")
tu_casa = Direccion("SIEMPRE VIVA 123", "SPRINGFIELD")
print(f"Identificador: {id(micasa)}")
print(f"Identificador: {id(tu_casa)}")