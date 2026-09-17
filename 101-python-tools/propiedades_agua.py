import numpy as np

# ── Tabla IAPWS-IF97 ──────────────────────────────────────────────────────────
T_tabla = np.array([
      0,    5,   10,   15,   20,   25,   30,   35,   40,   45,
     50,   55,   60,   65,   70,   75,   80,   85,   90,   95,
    100,  110,  120,  130,  140,  150,  160,  170,  180,  190,
    200,  210,  220,  230,  240,  250,  260,  270,  280,  290,
    300,  320,  340,  360,  374.14
])
P_sat_tabla = np.array([
    0.6113,   0.8726,   1.2281,   1.7057,   2.3393,   3.1693,
    4.2470,   5.6291,   7.3849,   9.5935,  12.352,   15.763,
   19.946,   25.041,   31.202,   38.597,   47.416,   57.867,
   70.182,   84.609,  101.325,  143.38,   198.67,   270.41,
  361.53,   476.16,   618.23,   792.59,  1002.8,   1255.2,
 1554.9,   1907.7,   2319.6,   2797.1,   3347.8,   3978.8,
 4694.3,   5503.0,   6413.2,   7436.0,   8587.9,  11284.0,
14601.0,  18666.0,  22089.0
])

def P_saturacion(T_C):
    """Presión de saturación del agua en kPa dado T en °C."""
    if not (0 <= T_C <= 374.14):
        raise ValueError(f"Temperatura {T_C}°C fuera del rango válido (0 - 374.14°C)")
    return float(np.interp(T_C, T_tabla, P_sat_tabla))

def molesAguaEnAire(T_C, HR_porcentaje, presionDeGas, molesAire):
    """Moles de H2O por mol de aire seco."""
    presionSaturacionAgua   = P_saturacion(T_C)
    presionVaporEnAire = (HR_porcentaje / 100) * presionSaturacionAgua
    ratioPresiones  = presionVaporEnAire / presionDeGas
    molesAguaPorHumedad = (ratioPresiones*molesAire)/(1 + ratioPresiones)
    return molesAguaPorHumedad 