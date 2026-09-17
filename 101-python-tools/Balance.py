# Balance de ecuacion de etanol (alcohol) con aire a presión a la proporcion 
# de 1 kmol x O2 y 3.76 kmol de N2
# Ecuación quimica:
# aC2H5OH + b(O2 + 3.76N2) + cH2O -> dCO2 + eCO + fH2O + gN2 + hO2
# Colocaremos dos opciones: combustion irregular 
# (con CO producido) o regular (estequiometrica o con exceso aire)
# para definir variables usamos ESTADOS y la siguiente nomenclatura
# (variable termodinamica)(Estado: entrada o salida, 1, 2 o 3 etc)(Sustancia)(descripcion Proceso)
# temperaturaEntradaAire, presionEntradaAireCombustion, presionEntradaAireCompresion
from sympy import symbols, Eq, solve, Matrix
from propiedades_agua import P_saturacion, molesAguaEnAire  # <-- importa solo lo que necesitas

def Balance():
    a, b, c, d, e, f, g, h = symbols('a b c d e f g h', positive=True)
    
    # Entradas de usuario
    tipoCombustion = input("¿La combustión es regular o irregular?").lower().strip() # el .lower() hace que pase a minusculas todo el texto
    presionEntradaAire = float(input("¿Cuál es la presión de entrada del aire? (kPa)?"))
    temperaturaEntradaAire = float(input("¿Cuál es la temperatura de entrada del aire? (°C)?"))
    humedadRelativa = float(input("Indica el % de humedad: "))
    factorExceso = float(input("Ingresa el porcentaje de exceso aire en orden del 100%"))

    # Calculo de coeficientes en cantidades molares
    # Ecuación aC2H5OH + b(O2 + 3.76N2) + -cH2O-  =>  dCO2 + -eCO- + fH2O + gN2 + -hO2-
    # priero se calculan coef. para ec. estequiometrica, al final se obtienen con aire de exceso si es que hay
    # el coeficiente "c" se obtiene por después y se le suma al coeficiente "f" en los productos
    if tipoCombustion == "regular":
        ecuaciones = [              
            Eq(2*a, d),                         # C: 2a = d
            Eq(6*a, 2*f),                       # H: 6a = 2f
            Eq(a + 2*b, 2*d + f),               # O: a + 2b = 2d + f
            Eq(3.76*2*b, 2*g),                  # N: 3.76(2)b = 2g
        ]
        solucion = solve(ecuaciones + [Eq(a, 1)], [a, b, d, f, g])

        # Valores numericos de coeficientes, ya no simbolicos  
        dvalorNumerico = float(solucion[d])
        bvalorNumerico = float(solucion[b])
        bvalorNumerico = bvalorNumerico*(factorExceso/100)
        molesAire = bvalorNumerico
        molesCombustible = avalorNumerico
        avalorNumerico = float(solucion[a])
        evalorNumerico = 0
        fvalorNumerico = float(solucion[f])
        gvalorNumerico = float(solucion[g])
        hvalorNumerico = bvalorNumerico - float(solucion[b])
        
        # Calculo de humedad
        if humedadRelativa > 0:
            cvalorNumerico = molesAguaEnAire(temperaturaEntradaAire, humedadRelativa, presionEntradaAire, molesAire) 
            print(f"Moles de agua por mol de aire seco(c): {cvalorNumerico:6f}")     
        else:
            cvalorNumerico = 0
        fvalorNumerico = cvalorNumerico + fvalorNumerico
    else:
        print("Combustion irregular - En Desarrollo . . .")
        # Para este caso, habria que saber la temp a la que quemo el combustible para suponer
        # una cantidad de monoxido de carbono y así particionar los moles del etanol
    
    ecuacionBalanceada = [
        avalorNumerico,
        bvalorNumerico,
        cvalorNumerico,
        dvalorNumerico,
        evalorNumerico,
        fvalorNumerico,
        gvalorNumerico,
        hvalorNumerico
        ] 
    
    relacionCombustibleAire = molesCombustible / molesAire
    relacion
    print(f"La relación combustible / aire es:")
    print(f"El valor de combustible estequiometrico(a): {avalorNumerico:2f}")
    print(f"El valor de aire estequiometrico(b): {bvalorNumerico:2f}")
    print(ecuacionBalanceada) 
    return ecuacionBalanceada 
Balance()