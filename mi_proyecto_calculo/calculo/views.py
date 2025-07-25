# mi_proyecto_calculo/calculo/views.py

from django.shortcuts import render
import os
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64
import math # <-- Nueva importación para funciones matemáticas (sqrt)

def grafica_3d_view(request):
    # Define la ruta del archivo .txt
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txt_file_path = os.path.join(project_root, 'src', 'Storage', 'GaussJordan.txt')

    puntos = []
    error_message = None
    graph_image_base64 = None
    distances = [] # <-- Lista para almacenar las distancias

    try:
        with open(txt_file_path, 'r') as f:
            first_line = f.readline()

            for i, line in enumerate(f):
                if i >= 5:
                    break

                line = line.strip()
                if not line:
                    continue

                match = re.match(r'x:([-+]?\d*\.?\d+)#y:([-+]?\d*\.?\d+)#z:([-+]?\d*\.?\d+)', line)
                if match:
                    try:
                        x = float(match.group(1))
                        y = float(match.group(2))
                        z = float(match.group(3))
                        puntos.append([x, y, z])
                    except ValueError:
                        error_message = f"Error: Coordenadas no numéricas en la línea: {line}"
                        puntos = []
                        break
                else:
                    error_message = f"Error: Formato de línea incorrecto: '{line}'. Esperado 'x:NN#y:NN#z:NN'."
                    puntos = []
                    break

        # --- Lógica de cálculo de distancias ---
        if puntos:
            # Función auxiliar para calcular la distancia euclidiana entre dos puntos 3D
            def calculate_distance(p1, p2):
                return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

            # Iterar sobre todos los pares de puntos para calcular las distancias
            num_points = len(puntos)
            for i in range(num_points):
                for j in range(i + 1, num_points): # Evita duplicados y distancia de un punto a sí mismo
                    p1_idx = i + 1 # Para mostrar P1, P2 en lugar de P0, P1
                    p2_idx = j + 1
                    dist = calculate_distance(puntos[i], puntos[j])
                    distances.append({
                        'point1': f'Punto {p1_idx} ({puntos[i][0]:.2f}, {puntos[i][1]:.2f}, {puntos[i][2]:.2f})',
                        'point2': f'Punto {p2_idx} ({puntos[j][0]:.2f}, {puntos[j][1]:.2f}, {puntos[j][2]:.2f})',
                        'distance': f'{dist:.4f}' # Formatear la distancia a 4 decimales
                    })
        # --- Fin Lógica de cálculo de distancias ---


        if puntos:
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection='3d')

            x_coords = [p[0] for p in puntos]
            y_coords = [p[1] for p in puntos]
            z_coords = [p[2] for p in puntos]
             # --- AÑADE ESTE BLOQUE PARA LOS COLORES ---
        # Define una lista de colores. Asegúrate de tener suficientes colores para el máximo de 5 puntos.
        # Puedes usar nombres de colores (ej. 'red', 'green', 'blue') o códigos hexadecimales ('#FF0000')
            colors = ['blue', 'green', 'red', 'purple', 'orange']
        # Asegúrate de no exceder el número de colores disponibles si tienes más puntos.
        # Tomamos un subconjunto de colores si tenemos menos puntos que colores definidos
            point_colors = colors[:len(puntos)]
        # --- FIN DEL BLOQUE A AÑADIR ---
            ax.scatter(x_coords, y_coords, z_coords, c=point_colors, marker='o', s=100)

            if len(puntos) >= 2:
                ax.plot(x_coords, y_coords, z_coords, color='red', linestyle='-')

            ax.set_xlabel('Eje X')
            ax.set_ylabel('Eje Y')
            ax.set_zlabel('Eje Z')
            ax.set_title('Gráfica 3D de Puntos y Líneas')

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            graph_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close(fig)

        if not puntos and not error_message:
            error_message = "No se encontraron puntos válidos en el archivo para graficar."

        print(f"Puntos leídos desde {txt_file_path}: {puntos}")
        print(f"Distancias calculadas: {distances}") # Para depuración en la terminal

    except FileNotFoundError:
        error_message = f"Error: El archivo de puntos no se encontró en la ruta esperada: {txt_file_path}"
    except Exception as e:
        error_message = f"Ocurrió un error inesperado al leer el archivo: {e}"

    context = {
        'puntos': puntos,
        'error_message': error_message,
        'graph_image_base64': graph_image_base64,
        'distances': distances, # <-- Pasamos las distancias a la plantilla
    }
    return render(request, 'calculo/grafica_3d.html', context)