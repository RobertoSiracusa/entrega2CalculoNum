import numpy as np
from matriz_formula import MatrizFormula

# Edita aquí las matrices que quieras usar:
A = np.array([[1, 0], [0, 1]])  # Matriz identidad 2x2
B = np.array([[2, 2], [2, 2]])  # Matriz de doses 2x2
C = np.array([[3, 3], [3, 3]])  # Matriz de treses 2x2

# Leer fórmulas desde un archivo txt
with open('formulas.txt', 'r') as f:
    formulas = [line.strip() for line in f if line.strip()]

for idx, formula in enumerate(formulas):
    print(f'Procesando fórmula {idx+1}: {formula}')
    mf = MatrizFormula(A, B, C, formula)
    resultado = mf.ejecutar_formula()
    if resultado is not None:
        bin_filename = f'resultado_{idx+1}.bin'
        mf.guardar_resultado_bin(bin_filename)
        print(f'Resultado guardado en {bin_filename}\n')
    else:
        print(f'Error: {mf.error}\n') 