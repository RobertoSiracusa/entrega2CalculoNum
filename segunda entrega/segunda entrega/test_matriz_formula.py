import numpy as np
from matriz_formula import MatrizFormula

# Matrices de prueba
A = np.array([[28, -1, 28], [-11, -8,19], [-9, 13, 27]])
B = np.array([[13, 30,-8], [22, 18,17], [8, 28, -1]])
C = np.array([[-9, 25,-3], [-19,-29, -23], [-7, -13, 27]])

# Fórmulas de prueba
formulas = [
    '2*A + 3*B - C',   # válida
    'A**B'                # inválida (producto elemento a elemento)
]

for formula in formulas:
    print(f'Probando fórmula: {formula}')
    mf = MatrizFormula(A, B, C, formula)
    resultado = mf.ejecutar_formula()
    if resultado is not None:
        print('Resultado numérico:')
        print(resultado)
    else:
        print('Error detectado:')
        print(mf.error)
    print('-'*40) 