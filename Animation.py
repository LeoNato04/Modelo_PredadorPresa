import pygame
import os
import random
import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image, ImageTk

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 VALORES INICIALES

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Configuración de posición
os.environ['SDL_VIDEO_WINDOW_POS'] = "500,230"
ASSETS_DIR = os.path.join(os.getcwd(), 'assets')

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 1400, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Modelo Depredador-Presa de Lotka-Volterra")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)  
GRAY = (200, 200, 200)

# Cargar imágenes desde la carpeta 'assets'
rabbit_image = pygame.image.load(os.path.join(ASSETS_DIR, 'conejo.png'))
fox_image = pygame.image.load(os.path.join(ASSETS_DIR, 'zorro.png'))
rabbit_image = pygame.transform.scale(rabbit_image, (30, 30))
fox_image = pygame.transform.scale(fox_image, (40, 40))

# Configuración inicial
clock = pygame.time.Clock()
trail_length = 50
elapsed_months = 0

# Parámetros del modelo de Lotka-Volterra ajustados
r1 = 0.8
a1 = 0.007
r2 = 0.2
a2 = 0.0004
K = 1000

# Condiciones iniciales
prey_population = 400
predator_population = 5

# Fuente para el texto
font = pygame.font.SysFont(None, 30)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
FUNCIONES PRINCIPALES

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Función para mover las presas
def move_prey(position, speed):
    position[0] += random.randint(-speed, speed)
    position[1] += random.randint(-speed, speed)

    # Mantener dentro de la pantalla
    position[0] = max(15, min(screen_width - 15, position[0]))
    position[1] = max(15, min(screen_height - 15, position[1]))

    return position

# Función para mover el depredador hacia la presa
def move_predator(predator_pos, prey_pos, speed):
    direction = [prey_pos[0] - predator_pos[0], prey_pos[1] - predator_pos[1]]
    distance = math.sqrt(direction[0]**2 + direction[1]**2)
    if distance > 0:
        direction = [direction[0] / distance, direction[1] / distance]
        predator_pos[0] += direction[0] * speed
        predator_pos[1] += direction[1] * speed

    return predator_pos

# Función para actualizar las poblaciones de conejos y zorros
def update_populations(prey_population, predator_population, dt, r1, a1, r2, a2, K):
    # Ecuaciones de Lotka-Volterra
    dR = (r1 * prey_population * (1 - prey_population / K) - a1 * prey_population * predator_population) * dt
    dP = (a2 * prey_population * predator_population - r2 * predator_population) * dt

    # Actualizar las poblaciones
    prey_population += dR
    predator_population += dP

    # Asegurarse de que las poblaciones no sean negativas
    prey_population = max(0, prey_population)
    predator_population = max(0, predator_population)

    return prey_population, predator_population

# Función para dibujar el texto en pantalla
def draw_population_info(prey_population, predator_population, months):
    # Mostrar la cantidad de conejos y zorros en la esquina superior izquierda
    prey_text = font.render(f"Conejos: {int(prey_population)}", True, BLACK)
    predator_text = font.render(f"Zorros: {int(predator_population)}", True, BLACK)

    # Mostrar el contador de meses en la esquina superior izquierda
    months_text = font.render(f"Meses: {months}", True, BLACK)

    screen.blit(prey_text, (1180, 470))
    screen.blit(predator_text, (1180, 500))
    screen.blit(months_text, (950, 500))

# Función para crear el gráfico
def create_graph(prey_data, predator_data, months):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(range(len(prey_data)), prey_data, label="Conejos")
    ax.plot(range(len(predator_data)), predator_data, label="Zorros", color='r')
    ax.set_xlabel("Meses")
    ax.set_ylabel("Población")
    ax.set_title("Poblaciones de Conejos y Zorros")
    ax.legend()

    canvas = FigureCanvas(fig)
    canvas.draw()

    # Renderizar el gráfico en pygame
    canvas_width, canvas_height = canvas.get_width_height()
    raw_data = bytes(canvas.buffer_rgba())  # Convertir memoryview a bytes
    surface = pygame.image.fromstring(raw_data, (canvas_width, canvas_height), "RGBA")

    plt.close(fig)

    return surface


# Función para crear la ventana de parámetros con Tkinter
def create_tkinter_window():
    window = tk.Tk()
    window.title("Parámetros del Modelo")
    window.geometry("420x600+30+200")

    # fuente
    font = ("Arial", 14)

    # Subtítulo
    tk.Label(window, text="Tasas de los parámetros:", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Crear las etiquetas y entradas para los parámetros
    tk.Label(window, text="Crecimiento de conejos (r1):", font=("Arial", 12), anchor="e").grid(row=1, column=0, sticky="e", padx=5)
    r1_entry = tk.Entry(window)
    r1_entry.grid(row=1, column=1)
    r1_entry.insert(tk.END, str(r1))

    tk.Label(window, text="Caza de conejos por zorros (a1):", font=("Arial", 12), anchor="e").grid(row=2, column=0, sticky="e", padx=5)
    a1_entry = tk.Entry(window)
    a1_entry.grid(row=2, column=1)
    a1_entry.insert(tk.END, str(a1))

    tk.Label(window, text="Mortalidad de zorros (r2):", font=("Arial", 12), anchor="e").grid(row=3, column=0, sticky="e", padx=5)
    r2_entry = tk.Entry(window)
    r2_entry.grid(row=3, column=1)
    r2_entry.insert(tk.END, str(r2))

    tk.Label(window, text="Conversión de presas a zorros (a2):", font=("Arial", 12), anchor="e").grid(row=4, column=0, sticky="e", padx=5)
    a2_entry = tk.Entry(window)
    a2_entry.grid(row=4, column=1)
    a2_entry.insert(tk.END, str(a2))

    tk.Label(window, text="Capacidad de carga (K):", font=("Arial", 12), anchor="e").grid(row=5, column=0, sticky="e", padx=5)
    K_entry = tk.Entry(window)
    K_entry.grid(row=5, column=1)
    K_entry.insert(tk.END, str(K))


    # Parámetros iniciales
    tk.Label(window, text="Parámetros iniciales:", font=("Arial", 16, "bold")).grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(window, text="Población inicial de conejos (P):", font=("Arial", 12), anchor="e").grid(row=7, column=0, sticky="e", padx=5)
    prey_entry = tk.Entry(window)
    prey_entry.grid(row=7, column=1)
    prey_entry.insert(tk.END, str(prey_population))

    tk.Label(window, text="Población inicial de zorros (D):", font=("Arial", 12), anchor="e").grid(row=8, column=0, sticky="e", padx=5)
    predator_entry = tk.Entry(window)
    predator_entry.grid(row=8, column=1)
    predator_entry.insert(tk.END, str(predator_population))

    # Cargar la imagen de las ecuaciones desde la carpeta 'assets'
    equations_img = Image.open(os.path.join(ASSETS_DIR, 'equations.png'))
    equations_img = equations_img.resize((300, 150))  # Redimensionar la imagen si es necesario
    equations_img_tk = ImageTk.PhotoImage(equations_img)

    # Muestra la imagen redimensionada
    tk.Label(window, image=equations_img_tk).grid(row=10, column=0, columnspan=2, pady=10)
    window.image = equations_img_tk  # Mantener una referencia a la imagen

    # Funciones de los botones
    def start_simulation():
        global r1, a1, r2, a2, K, simulation_running
        r1 = float(r1_entry.get())
        a1 = float(a1_entry.get())
        r2 = float(r2_entry.get())
        a2 = float(a2_entry.get())
        K = float(K_entry.get())
        simulation_running = True
        window.quit()

    def close_windows():
        global simulation_running, running
        simulation_running = False
        running = False
        window.quit()
        window.destroy()

    # Función de reinicio 
    def restart_simulation():
        global simulation_running, running, elapsed_months, prey_population, predator_population, prey_data, predator_data
        elapsed_months = 0
        prey_population = 400
        predator_population = 5
        prey_data = []
        predator_data = []
        simulation_running = False

        window.quit()
        create_tkinter_window()


    # BOTONES
    # Botón para iniciar la simulación
    start_button = tk.Button(window, text="Iniciar Simulación", font=font, command=start_simulation)
    start_button.grid(row=11, column=0, columnspan=2)

    # Añadir el botón de reiniciar
    restart_button = tk.Button(window, text="Reiniciar", font=font, command=restart_simulation)
    restart_button.grid(row=12, column=0, columnspan=2, pady=10)

   # Botón para cerrar las ventanas
    close_button = tk.Button(window, text="Cerrar", font=font, command=close_windows)
    close_button.grid(row=13, column=0, columnspan=2, pady=10)

    window.mainloop()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 INTERFAZ DE TKINTER

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Bucle principal
running = True
prey_data = []
predator_data = []
simulation_running = False 

# Crear la ventana de parámetros de Tkinter
create_tkinter_window()

while running:
    screen.fill(WHITE)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Si la simulación está corriendo, actualizamos la población
    if simulation_running:
        dt = clock.get_time() / 1000.0
        prey_population, predator_population = update_populations(prey_population, predator_population, dt, r1, a1, r2, a2, K)

        # Actualizar el contador de meses basándonos en un incremento constante
        elapsed_months += dt * 4
        current_months = int(elapsed_months)

        # Guardar los datos de la población
        prey_data.append(prey_population)
        predator_data.append(predator_population)

        # Dibujar las presas (conejos)
        for i in range(int(prey_population)):
            x, y = random.randint(0, int(screen_width * 0.6) - 30), random.randint(0, screen_height - 30)
            screen.blit(rabbit_image, (x, y))

        # Dibujar los depredadores (zorros)
        for i in range(int(predator_population)):
            x, y = random.randint(0, int(screen_width * 0.6) - 30), random.randint(0, screen_height - 30)
            screen.blit(fox_image, (x, y))

        # Dibujar la tabla con la población y el contador de meses
        draw_population_info(prey_population, predator_population, current_months)

        # Crear el gráfico
        graph_surface = create_graph(prey_data, predator_data, current_months)

        # Dibujar el gráfico en la parte derecha de la pantalla
        screen.blit(graph_surface, (int(screen_width * 0.3) + 450, 20))

    pygame.display.flip()
    clock.tick(30)