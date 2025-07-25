import numpy as np
import os

# Cambia esto si tus matrices no son 2x2
shape = (3, 3)

# Buscar todos los archivos .bin en la carpeta actual
dir_actual = os.path.dirname(__file__)
archivos_bin = [f for f in os.listdir(dir_actual) if f.endswith('.bin')]

if not archivos_bin:
    print('No se encontraron archivos .bin en la carpeta.')
else:
    for archivo in sorted(archivos_bin):
        ruta = os.path.join(dir_actual, archivo)
        try:
            matriz = np.fromfile(ruta, dtype=np.float64).reshape(shape)
            print(f'Archivo: {archivo}')
            print(matriz)
            print('-'*30)
        except Exception as e:
            print(f'No se pudo leer {archivo}: {e}') 