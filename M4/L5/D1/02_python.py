# Ejemplo 2: ZeroDivisionError

def division_segura(a: float, b: float) -> float:
    return a / b  # lanza ZeroDivisionError si b == 0

print((division_segura(5, 0)))