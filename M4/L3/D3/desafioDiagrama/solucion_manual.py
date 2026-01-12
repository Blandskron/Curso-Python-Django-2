class Holding():
    pass

class Empresa(Holding):
    pass

class Area(Empresa):
    pass

class Usuario():
    pass

class Inversionista(Usuario):
    pass

class Gerente(Usuario):
    pass

class Empleado(Usuario):
    pass

class Trabajador(Empleado):
    pass

    def crear_documento():
        doc = Documento()
        return doc

class Jefatura(Empleado):
    pass

    def crear_documento():
        doc = Documento()
        return doc

class Documento:
    pass

    def compartir_documento(compartir_holding):
        doc = compartir_holding()
        pass

class DocumentoHolding(Documento, Holding):
    pass

    def compartir_holding(compartir_empresa):
        doc = compartir_empresa()

class DocumentoEmpresa(Documento, Empresa):
    pass

    def compartir_empresa(compartir_area):
        doc = compartir_area()

class DocumentoArea(Documento, Area):
    pass

    def compartir_area(compartir_persona):
        doc = compartir_persona

class DocumentoPersona(Documento, Usuario):
    pass

    def compartir_persona():
        per = []
