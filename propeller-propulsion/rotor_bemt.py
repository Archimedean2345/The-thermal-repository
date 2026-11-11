"""
BEMT en hover: teoria combinada de elemento de alabe + momento
con perdidas de punta de Prandtl.

Calcula: empuje, potencia (inducida + perfil), par, FM,
distribuciones radiales y cargas por alabe (flap, lag, centrifuga, conicidad).
Dependencias: numpy, matplotlib.
"""
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARAMETROS
# ============================================================
p = dict(
    N=3,                # numero de palas
    R=1.0,              # radio [m]
    r_root=0.15,        # corte de raiz r0/R [-]
    # taper_ratio=0.8,    # relación de cuerdas de punta y raiz
    c_root=0.094,       # cuerda en la raiz [m]
    c_tip=0.094,
    tw_deg=-8.0,        # torsion lineal raiz -> punta [deg] (negativa = punta con menos paso)
    V_tip=200.0,        # velocidad de punta [m/s]
    rho=1.225,          # densidad [kg/m3]
    a=5.73,             # pendiente de sustentacion [1/rad]
    Cl_max=1.3,         # C_l de entrada en perdida
    d0=0.0110,          # polar del perfil: Cd = d0 + d1*alpha + d2*alpha^2
    d1=-0.025,
    d2=0.65,
    m_lin=0.8,          # masa lineal del alabe [kg/m] (supuesto, solo para cargas)
    n=100,              # numero de elementos radiales
)
T_meta = 170 * 9.81     # empuje meta [N] -> se ajusta el colectivo para lograrlo

# ============================================================
# BEMT
# theta0_deg = paso colectivo medido a 75% del radio
# ============================================================
def bemt(theta0_deg, N, R, r_root, c_root, c_tip, tw_deg, V_tip, rho,
         a, Cl_max, d0, d1, d2, m_lin, n):
    # --- Discretizacion (centros de elemento) ---
    bordes = np.linspace(r_root, 1, n + 1)
    r  = 0.5 * (bordes[1:] + bordes[:-1])          # r = y/R
    dr = (1 - r_root) / n

    # --- Geometria local ---
    c   = c_root + (c_tip - c_root) * (r - r_root) / (1 - r_root)
    sig = N * c / (np.pi * R)                      # solidez local
    th  = np.radians(theta0_deg + tw_deg * (r - 0.75))

    # --- Inflow con perdida de punta de Prandtl (iterativo) ---
    # lambda(r) = sigma*a/(16F) * [sqrt(1 + 32 F theta r/(sigma a)) - 1]
    # F = (2/pi) arccos(exp(-f)),  f = (N/2)(1-r)/lambda
    def inflow(F):
        # max(...,0) evita raiz negativa si alguna seccion queda con paso < 0
        return sig * a / (16 * F) * (np.sqrt(np.maximum(1 + 32 * F * th * r / (sig * a), 0)) - 1)

    F = np.ones_like(r)
    for _ in range(100):
        lam = inflow(F)
        f = 0.5 * N * (1 - r) / np.maximum(lam, 1e-8)
        F_nuevo = 2 / np.pi * np.arccos(np.exp(-f))
        if np.max(np.abs(F_nuevo - F)) < 1e-8:
            break
        F = F_nuevo
    F = F_nuevo
    lam = inflow(F)

    # --- Aerodinamica local ---
    phi   = lam / r                                # angulo de inflow [rad]
    alpha = th - phi                               # angulo de ataque [rad]
    Cl    = a * alpha
    Cd    = d0 + d1 * alpha + d2 * alpha**2

    # --- Coeficientes por elemento ---
    dCT  = 0.5 * sig * Cl * r**2 * dr              # empuje
    dCPi = lam * dCT                               # potencia inducida
    dCP0 = 0.5 * sig * Cd * r**3 * dr              # potencia de perfil
    CT, CPi, CP0 = dCT.sum(), dCPi.sum(), dCP0.sum()
    CP = CPi + CP0

    # --- Dimensional ---
    A     = np.pi * R**2
    Omega = V_tip / R
    y, dy = r * R, dr * R
    T = CT * rho * A * V_tip**2
    P = CP * rho * A * V_tip**3
    Q = P / Omega

    # --- Cargas por alabe (respecto al eje del rotor) ---
    dT_b = dCT * rho * A * V_tip**2 / N            # empuje de cada elemento, un alabe [N]
    dQ_b = (dCPi + dCP0) * rho * A * V_tip**3 / Omega / N
    M_flap = np.sum(dT_b * y)                      # momento de flap en raiz [N*m]
    M_lag  = dQ_b.sum()                            # momento en el plano (lag) [N*m] = Q/N
    CF     = np.sum(m_lin * Omega**2 * y * dy)     # fuerza centrifuga en raiz [N]
    I_b    = np.sum(m_lin * y**2 * dy)             # inercia de flap [kg*m2]
    beta0  = M_flap / (I_b * Omega**2)             # conicidad (alabe articulado) [rad]

    P_ideal = T**1.5 / np.sqrt(2 * rho * A)

    return dict(
        T=T, P=P, Q=Q, CT=CT, CP=CP, CPi=CPi, CP0=CP0,
        FM=P_ideal / P, P_ideal=P_ideal, Omega=Omega, A=A,
        sigma=np.mean(sig), M_flap=M_flap, M_lag=M_lag, CF=CF, beta0=beta0,
        r_T=M_flap / dT_b.sum() / R,               # centro de empuje r/R
        # distribuciones
        r=r, y=y, lam=lam, F=F, alpha=alpha, Cl=Cl, Cd=Cd,
        dTdy=dT_b / dy, dQdy=dQ_b / dy,
        dPi_dy=dCPi * rho * A * V_tip**3 / dy, dP0_dy=dCP0 * rho * A * V_tip**3 / dy,
        Cl_max=Cl_max,
    )


# ============================================================
# TRIM: colectivo para el empuje meta (biseccion / goal seek)
# ============================================================
def goal_seek(f, objetivo, x_min, x_max, tol=1e-6, max_iter=100):
    for _ in range(max_iter):
        x_mid = (x_min + x_max) / 2
        if (f(x_min) - objetivo) * (f(x_mid) - objetivo) <= 0:
            x_max = x_mid
        else:
            x_min = x_mid
        if x_max - x_min < tol:
            break
    return (x_min + x_max) / 2


theta75 = goal_seek(lambda th: bemt(th, **p)["T"], T_meta, 0.0, 25.0)
s = bemt(theta75, **p)


# ============================================================
# RESULTADOS
# ============================================================
def fila(nombre, valor, unidad=""):
    print(f"{nombre:<30}{valor:>12.4f}  {unidad}")

print("=" * 56)
print("TRIM")
fila("Colectivo theta_75", theta75, "deg")
fila("RPM", s["Omega"] * 60 / (2 * np.pi), "rpm")
print("-" * 56)
print("ROTOR")
fila("Empuje T", s["T"], "N")
fila("Empuje T", s["T"] / 9.81, "kgf")
fila("C_T", s["CT"], "-")
fila("C_T/sigma", s["CT"] / s["sigma"], "-")
fila("Potencia total P", s["P"] / 1e3, "kW")
fila("  inducida", s["CPi"] / s["CP"] * s["P"] / 1e3, "kW")
fila("  perfil", s["CP0"] / s["CP"] * s["P"] / 1e3, "kW")
fila("Potencia ideal", s["P_ideal"] / 1e3, "kW")
fila("Figura de merito FM", s["FM"], "-")
fila("Par Q", s["Q"], "N*m")
print("-" * 56)
print("CARGAS POR ALABE (raiz)")
fila("Momento de flap", s["M_flap"], "N*m")
fila("Momento de lag (Q/N)", s["M_lag"], "N*m")
fila("Fuerza centrifuga", s["CF"], "N")
fila("Conicidad beta0", np.degrees(s["beta0"]), "deg")
fila("Centro de empuje r_T/R", s["r_T"], "-")
print("-" * 56)
i = np.argmax(s["Cl"])
fila("C_l maximo", s["Cl"][i], f"en r/R = {s['r'][i]:.2f}")
if s["Cl"].max() > s["Cl_max"]:
    print("  !! AVISO: secciones en perdida (C_l > Cl_max)")
print("=" * 56)


# ============================================================
# GRAFICAS
# ============================================================
fig, ax = plt.subplots(2, 2, figsize=(11, 7))
r = s["r"]

ax[0, 0].plot(r, s["lam"], label="lambda (inflow)")
ax[0, 0].set_ylabel("lambda [-]")
ax00b = ax[0, 0].twinx()
ax00b.plot(r, s["F"], "--", color="gray", label="F Prandtl")
ax00b.set_ylabel("F [-]")
ax[0, 0].set_title("Inflow y perdida de punta")

ax[0, 1].plot(r, s["Cl"], label="C_l")
ax[0, 1].axhline(s["Cl_max"], ls="--", color="red", lw=0.8, label="C_l max")
ax[0, 1].set_ylabel("C_l [-]")
ax[0, 1].set_ylim(0, s["Cl_max"] * 1.1)
ax01b = ax[0, 1].twinx()
ax01b.plot(r, np.degrees(s["alpha"]), ":", color="gray")
ax01b.set_ylabel("alpha [deg] (punteado)")
ax[0, 1].set_title("C_l local vs perdida")
ax[0, 1].legend(loc="lower center")

ax[1, 0].plot(r, s["dTdy"])
ax[1, 0].set_ylabel("dT/dy por alabe [N/m]")
ax[1, 0].set_title("Distribucion de empuje")

ax[1, 1].plot(r, s["dPi_dy"] / 1e3, label="inducida")
ax[1, 1].plot(r, s["dP0_dy"] / 1e3, label="perfil")
ax[1, 1].set_ylabel("dP/dy rotor [kW/m]")
ax[1, 1].set_title("Distribucion de potencia")
ax[1, 1].legend()

for a_ in ax.flat:
    a_.set_xlabel("r/R")
    a_.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("bemt.png", dpi=120)
plt.show()