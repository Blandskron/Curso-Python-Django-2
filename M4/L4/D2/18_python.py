# Ejemplo 18: Uso de __slots__ en jerarquía

class NodoBase:
    __slots__ = ("valor",)

    def __init__(self, valor: int):
        self.valor = valor


class NodoConHijos(NodoBase):
    __slots__ = ("izq", "der")

    def __init__(self, valor: int, izq=None, der=None):
        super().__init__(valor)
        self.izq = izq
        self.der = der

# Hojas
nodo_1 = NodoConHijos(1)
nodo_3 = NodoConHijos(3)

# Nodo padre
raiz = NodoConHijos(2, izq=nodo_1, der=nodo_3)
