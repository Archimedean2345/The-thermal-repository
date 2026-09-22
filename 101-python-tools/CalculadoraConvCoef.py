# Convective heat transfer coefficient calculator
# Se seguiran las notas dejadas por Richard Nakka
# sobre el calculo del coef de transferencia de calor por convección
# "...The-thermal-repository\literature\srm-specific-literature\Tech notepad Conv. heat transf. coef. - R. Nakka.pdf"
#
# Implementa dos métodos:
#   1. Correlación clásica de tubo liso con flujo turbulento (Dittus-Boelter):
#         h = 0.023 * (k/Di) * Re^0.8 * Pr^0.33
#      valida para 2300 < Re < 1e6  y  0.6 < Pr < 500
#
#   2. Ecuación alternativa (Mark's Handbook for Mechanical Engineers, 8th ed.),
#      más aplicada directamente al análisis de motores cohete:
#         h = C * (Cp * G^0.8 / Di^0.2) * [1 + (Di/L)^0.7]
#      con C = 3.075 (S.I.) o C = 0.024 (unidades inglesas)

import math

# ---------------------------------------------------
# Método 1: Correlación de tubo liso (Dittus-Boelter)
# No se utilizará este método 
def reynolds(v, Di, rho, mu):
    """
    Numero de Reynolds.
    v   : velocidad del fluido [m/s]
    Di  : diametro interno del tubo/camara [m]
    rho : densidad del fluido [kg/m^3]
    mu  : viscosidad dinamica del fluido [Pa*s]
    """
    return (v * Di * rho) / mu

def prandtl(Cp, mu, k):
    """
    Numero de Prandtl.
    Cp : calor especifico del fluido [J/(kg*K)]
    mu : viscosidad dinamica del fluido [Pa*s]
    k  : conductividad termica del fluido [W/(m*K)]
    """
    return (Cp * mu) / k

def h_tubo_liso(v, Di, rho, mu, Cp, k, validar_rango=True):
    """
    Coeficiente de conveccion h [W/m^2-K] via la correlacion de tubo liso
    con flujo interno turbulento:
        h = 0.023 * (k/Di) * Re^0.8 * Pr^0.33

    Retorna un dict con h, Re y Pr para poder inspeccionar los valores
    intermedios y validar el rango de aplicabilidad.
    """
    Re = reynolds(v, Di, rho, mu)
    Pr = prandtl(Cp, mu, k)

    if validar_rango:
        if not (2300 < Re < 1e6):
            print(f"[Aviso] Re = {Re:.1f} fuera del rango valido (2300 < Re < 1e6).")
        if not (0.6 < Pr < 500):
            print(f"[Aviso] Pr = {Pr:.3f} fuera del rango valido (0.6 < Pr < 500).")

    h = 0.023 * (k / Di) * (Re ** 0.8) * (Pr ** 0.33)

    return {"h": h, "Re": Re, "Pr": Pr}


# -----------------------------------------------------------------
# Método 2: Ecuación de Mark's Handbook (aplicada a motores cohete)
def mass_velocity(w, S):
    """
    Velocidad masica G = w / S.
    w : flujo masico promedio a traves de la camara [kg/s]
    S : area de seccion transversal de la camara [m^2]
    """
    return w / S


def area_transversal(Di):
    """Area de seccion transversal circular a partir del diametro interno [m]."""
    return (math.pi / 4) * (Di ** 2)


def h_motor_cohete(Cp, w, Di, L, unidades="SI"):
    """
    Coeficiente de conveccion h via la ecuacion de Mark's Handbook:
        h = C * (Cp * G^0.8 / Di^0.2) * [1 + (Di/L)^0.7]

    Parametros (unidades SI por defecto):
        Cp : calor especifico de la mezcla de combustion [J/(g*K)] (SI, ver nota abajo)
        w  : flujo masico promedio a traves de la camara [kg/s]
        Di : diametro interno de la camara [m]
        L  : longitud de la camara [m]
        unidades : "SI" (C = 3.075) o "ingles" (C = 0.024)

    Nota: en el ejemplo de Nakka, Cp se usa en J/g-K (no J/kg-K) para que las
    unidades resultantes de h sean W/m^2-K con C = 3.075. Respetamos esa
    convencion tal como aparece en el documento fuente.

    Retorna un dict con h, G y S.
    """
    if unidades == "SI":
        C = 3.075
    elif unidades == "ingles":
        C = 0.024
    else:
        raise ValueError("unidades debe ser 'SI' o 'ingles'")

    S = area_transversal(Di)
    G = mass_velocity(w, S)

    h = C * (Cp * (G ** 0.8) / (Di ** 0.2)) * (1 + (Di / L) ** 0.7)

    return {"h": h, "G": G, "S": S}


# ----------------------------------------------------------
# Prueba rapida: reproduce el ejemplo del documento de Nakka
if __name__ == "__main__":
    # Motor con 1.50 kg de propelente KN-Sorbitol 65/35, tb = 1.1 s
    # Camara: 65 mm diametro x 400 mm longitud
    Wp = 1.50      # kg, peso de propelente
    tb = 1.1       # s, tiempo de quemado
    Di = 65 / 1000  # m
    L = 400 / 1000  # m
    Cp = 1.74      # J/g-K (Cp' / MW, segun Notepad #3)

    w = Wp / tb
    resultado = h_motor_cohete(Cp, w, Di, L, unidades="SI")

    print("Reproduccion del ejemplo de R. Nakka (Notepad #4):")
    print(f"  w = {w:.3f} kg/s")
    print(f"  G = {resultado['G']:.1f} kg/s-m^2")
    print(f"  h = {resultado['h']:.1f} W/m^2-K   (esperado: 1457 W/m^2-K)")