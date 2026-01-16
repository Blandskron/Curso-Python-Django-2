from calc import sumar

def test_sumar():
    assert sumar(2, 3) == 5
    assert sumar(-1, 1) == 0
    assert sumar(0, 0) == 0
    assert sumar(2.5, 2.5) == 5.0

if __name__ == "__main__":
    test_sumar()
    print("✅ Tests OK")
