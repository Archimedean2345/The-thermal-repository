# Calculadora de transferencia de calor 1-dimension
# Casos
#   1. Pared
#       a. fluido - pared - fluido
#           a1. fluido - pared1 - pared2 - fluido
#       b. atmosfera - solidoNucleo
#       c. atmosfera - anillo sin contacto con sólidos

# Inputs - menu interactivo 

def atmos_solido_fluido():
    print("Introduzca las variables:")


def atmos_solido_nucleo():
    print("Introduzca las variables:")

def atmos_anillo():
    print("Introduzca las variables:")

def menu():
    casos = {"1": ("Atmosfera - Sólido - Fluido", atmos_solido_fluido),
             "2": ("Atmosfera - Sólido con Nucleo", atmos_solido_nucleo),
             "3": ("Atmosfera - Anillo sin contacto", atmos_anillo),
             "4": ("Exit", None)}
    print("Calculadora de Transferencia de Calor - Selecciona el caso a tratar")
    while True:
        for k, v in casos.items():
            print(f"{k}. {v[0]}") # k -> the numbers from 1 to 3 || v -> the function or parameter located in the item
        c = input("> ").strip()
        if c == "3":
            break
        if c in casos:
            casos[c][1]()
        else:
            print("Invalid.")

if __name__ == "__main__":
    menu()
# Outputs