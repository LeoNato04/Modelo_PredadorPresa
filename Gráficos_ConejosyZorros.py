import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

'''''''''''''''''''''''''''
PARÁMETROS
-----------
'''''''''''''''''''''''''''
# Parámetros del modelo Lotka-Volterra
r1 = 0.1         # Tasa de crecimiento de las presas (conejos)
a1 = 0.005       # Tasa de depredación
r2 = 0.04        # Tasa de mortalidad de los depredadores (zorros)
a2 = 0.00004     # Tasa de conversión de presas en depredadores
K = 10000        # Capacidad de carga del ambiente para las presas

# Condiciones iniciales
P0 = 200         # Población inicial de presas
D0 = 10          # Población inicial de depredadores

'''''''''''''''''''''''''''
FUNCIONES
---------
'''''''''''''''''''''''''''
# Definición del modelo Lotka-Volterra
def lotka_volterra(y, t, r1, a1, r2, a2, K):
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Modelo Lotka-Volterra con Capacidad de Carga:
    dP/dt = r1 * P * (1 - P/K) - a1 * P * D    # Cambio en las presas
    dD/dt = a2 * P * D - r2 * D                # Cambio en los depredadores
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    P, D = y
    dP_dt = r1 * P * (1 - P / K) - a1 * P * D
    dD_dt = a2 * P * D - r2 * D
    return [dP_dt, dD_dt]

# Tiempo de simulación (en meses)
t_extended = np.linspace(0, 400, 1500)

# Resolver el sistema de ecuaciones diferenciales
solution_extended = odeint(lotka_volterra, [P0, D0], t_extended, args=(r1, a1, r2, a2, K))
P_extended, D_extended = solution_extended.T

'''''''''''''''''''''''''''
GRÁFICOS
--------
'''''''''''''''''''''''''''

# Gráfico 1: Evolución temporal de las poblaciones
plt.figure(figsize=(10, 6))
plt.plot(t_extended, P_extended, label='Conejos (presas)', color='blue')
plt.plot(t_extended, D_extended, label='Zorros (depredadores)', color='red')
plt.title('Evolución Temporal de las Poblaciones (Conejos y Zorros)', fontsize=16)
plt.xlabel('Tiempo (meses)', fontsize=14)
plt.ylabel('Tamaño de la Población', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico 2: Diagrama de Fase (Presas vs Depredadores)
plt.figure(figsize=(10, 6))
plt.plot(P_extended, D_extended, color='purple')
plt.title('Diagrama de Fase (Conejos vs Zorros)', fontsize=16)
plt.xlabel('Conejos (presas)', fontsize=14)
plt.ylabel('Zorros (depredadores)', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()