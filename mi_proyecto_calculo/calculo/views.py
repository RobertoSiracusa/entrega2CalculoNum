# mi_proyecto_calculo/calculo/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
import os
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64
import math
import sys
import subprocess
import mimetypes
import datetime

def grafica_3d_view(request):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txt_file_path = os.path.join(project_root, 'src', 'Storage', 'GaussJordan.txt')

    puntos = []
    error_message = None
    graph_image_base64 = None
    distances = []
    
    execution_count = request.session.get('execution_count', 0)
    max_executions = 5
    
    storage_files = get_storage_files()

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

        if puntos:
            
            def calculate_distance(p1, p2):
                return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

            
            num_points = len(puntos)
            for i in range(num_points):
                for j in range(i + 1, num_points): 
                    p1_idx = i + 1 
                    p2_idx = j + 1
                    dist = calculate_distance(puntos[i], puntos[j])
                    distances.append({
                        'point1': f'Punto {p1_idx} ({puntos[i][0]:.2f}, {puntos[i][1]:.2f}, {puntos[i][2]:.2f})',
                        'point2': f'Punto {p2_idx} ({puntos[j][0]:.2f}, {puntos[j][1]:.2f}, {puntos[j][2]:.2f})',
                        'distance': f'{dist:.4f}' 
                    })
       


        if puntos:
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection='3d')

            x_coords = [p[0] for p in puntos]
            y_coords = [p[1] for p in puntos]
            z_coords = [p[2] for p in puntos]
             
            colors = ['blue', 'green', 'red', 'purple', 'orange']
        
            point_colors = colors[:len(puntos)]
        
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
        print(f"Distancias calculadas: {distances}")

    except FileNotFoundError:
        error_message = f"Error: El archivo de puntos no se encontró en la ruta esperada: {txt_file_path}"
    except Exception as e:
        error_message = f"Ocurrió un error inesperado al leer el archivo: {e}"

    context = {
        'puntos': puntos,
        'error_message': error_message,
        'graph_image_base64': graph_image_base64,
        'distances': distances,
        'execution_count': execution_count,
        'max_executions': max_executions,
        'can_execute': execution_count < max_executions,
        'storage_files': storage_files,
    }
    return render(request, 'calculo/grafica_3d.html', context)

def ejecutar_main_view(request):
    
    if request.method == 'POST':
        
        execution_count = request.session.get('execution_count', 0)
        max_executions = 5
        
        if execution_count >= max_executions:
            messages.error(request, f'Has alcanzado el máximo de {max_executions} ejecuciones permitidas.')
            return redirect('calculo:grafica_3d')
        
        try:
            
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            main_script_path = os.path.join(project_root, 'src', 'main.py')
            
            original_cwd = os.getcwd()
            os.chdir(project_root)
            
            try:
                
                result = subprocess.run([sys.executable, main_script_path], 
                                      capture_output=True, 
                                      text=True, 
                                      cwd=project_root)
                
                
                request.session['execution_count'] = execution_count + 1
                request.session.save()
                
                if result.returncode == 0:
                    messages.success(request, f'Programa ejecutado exitosamente. Ejecución #{execution_count + 1} de {max_executions}.')
                    if result.stdout:
                        messages.info(request, f'Salida: {result.stdout}')
                else:
                    messages.warning(request, f'El programa se ejecutó pero hubo advertencias. Código de salida: {result.returncode}')
                    if result.stderr:
                        messages.error(request, f'Errores: {result.stderr}')
                
            finally:
                
                os.chdir(original_cwd)
                
        except Exception as e:
            messages.error(request, f'Error al ejecutar el programa: {str(e)}')
    
    return redirect('calculo:grafica_3d')

def reset_execution_count_view(request):
    
    if request.method == 'POST':
        request.session['execution_count'] = 0
        request.session.save()
        messages.success(request, 'Contador de ejecuciones reiniciado.')
    
    return redirect('calculo:grafica_3d')

def get_storage_files():

    try:
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storage_path = os.path.join(project_root, 'src', 'Storage')
        
        if not os.path.exists(storage_path):
            return []
        
        files_info = []
        for filename in os.listdir(storage_path):
            file_path = os.path.join(storage_path, filename)
            
            
            if os.path.isfile(file_path):
                
                stat = os.stat(file_path)
                file_size = stat.st_size
                
                
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                
                mod_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in ['.txt', '.log']:
                    file_type = 'Texto'
                elif file_ext == '.bin':
                    file_type = 'Binario'
                else:
                    file_type = 'Otro'
                
                files_info.append({
                    'name': filename,
                    'size': size_str,
                    'size_bytes': file_size,
                    'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'type': file_type,
                    'extension': file_ext
                })
        
        files_info.sort(key=lambda x: x['modified'], reverse=True)
        
        return files_info
        
    except Exception as e:
        return []

def download_file_view(request, filename):

    try:

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storage_path = os.path.join(project_root, 'src', 'Storage')
        file_path = os.path.join(storage_path, filename)
        
        
        if not os.path.exists(file_path) or not file_path.startswith(storage_path):
            raise Http404("Archivo no encontrado")
        
        
        if not os.path.isfile(file_path):
            raise Http404("Archivo no encontrado")
        
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
    except Exception as e:
        raise Http404("Error al descargar el archivo")