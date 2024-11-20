import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

'''''''''''''''''''''''''''
PARÁMETROS
-----------
'''''''''''''''''''''''''''
# Parámetros del modelo básico'
r1 = 0.1        # tasa de crecimiento de las presas
a1 = 0.02       # tasa de depredación
r2 = 0.1        # tasa de mortalidad de los depredadores
a2 = 0.01       # tasa de conversión de presas en depredadores

# [presas, depredadores]
initial_conditions = [40, 9]


'''''''''''''''''''''''''''
Función de la simulación
------------------------
'''''''''''''''''''''''''''
# Sistema de ecuaciones diferenciales
def lotka_volterra(y, t, r1, a1, r2, a2):

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Ecuaciones del modelo de Lotka-Volterra (Modelo básico): 
    dP/dt = r1 * P - a1 * P * D     Cambio en la población de presas
    dD/dt = a2 * P * D - r2 * D     Cambio en la población de depredadores
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    presa, depredador = y
    dpresa_dt = r1 * presa - a1 * presa * depredador
    ddepredador_dt = a2 * presa * depredador - r2 * depredador
    return [dpresa_dt, ddepredador_dt]

# Tiempo de simulación
t = np.linspace(0, 200, 1000)

# Resolver las ecuaciones diferenciales
solution = odeint(lotka_volterra, initial_conditions, t, args=(r1, a1, r2, a2))
presas, depredadores = solution.T


'''''''''''''''''''''''''''
GRÁFICOS
---------
'''''''''''''''''''''''''''
# Gráfico 1: Oscilaciones poblacionales en el tiempo
plt.figure(figsize=(12, 6))
plt.plot(t, presas, label='Presas', color='green')
plt.plot(t, depredadores, label='Depredadores', color='red')
plt.title('Dinámica Poblacional de Presas y Depredadores', fontsize=16)
plt.xlabel('Tiempo', fontsize=14)
plt.ylabel('Población', fontsize=14)
plt.legend(fontsize=12)
plt.grid()
plt.show()

# Gráfico 2: Diagrama de fases (presa vs depredador)
plt.figure(figsize=(8, 8))
plt.plot(presas, depredadores, color='blue')
plt.title('Diagrama de Fases: Presas vs Depredadores', fontsize=16)
plt.xlabel('Población de Presas', fontsize=14)
plt.ylabel('Población de Depredadores', fontsize=14)
plt.grid()
plt.show()