import numpy as np
import re

class MatrizFormula:
    """
    Clase para validar y ejecutar fórmulas con matrices reales.
    
    Ejemplos de fórmulas válidas:
        '2*A + 3*B - C'
        'A @ B + 2*C'
        'A - B'
        '3*A'
        'A @ B'
    Ejemplos de fórmulas inválidas:
        'A*B'      # Producto elemento a elemento (no permitido)
        'A/B'      # División no permitida
        'A**2'     # Potencias no permitidas
        'A @ B @ C' # Solo si las dimensiones son compatibles
    """
    def __init__(self, A: np.ndarray, B: np.ndarray, C: np.ndarray, formula: str):
        self.A = A
        self.B = B
        self.C = C
        self.formula = formula
        self.resultado = None
        self.error = None

    def validar_formula(self):
        """
        Valida si la fórmula es aplicable a las matrices dadas.
        Si no es válida, guarda la justificación en notación de conjuntos en self.error.
        """
        # Solo se permiten: +, -, *, números reales, @ (producto matricial)
        # No se permite: *, /, ** entre matrices, funciones, etc.
        expr = self.formula.replace(' ', '')
        # Validar que solo hay A, B, C, números, +, -, *, @, paréntesis
        if re.search(r'[^ABC0-9+\-*@().]', expr):
            self.error = '{x ∈ Fórmula | símbolo no permitido en x}'
            return False
        # Validar que no hay producto elemento a elemento (A*B)
        if re.search(r'([ABC])\*([ABC])', expr):
            self.error = '{x ∈ Fórmula | producto elemento a elemento no permitido}'
            return False
        # Validar que no hay división ni potencias
        if '/' in expr or '**' in expr:
            self.error = '{x ∈ Fórmula | operación no permitida (/, **)}'
            return False
        # Validar producto matricial: dimensiones compatibles
        # Buscar todos los productos matriciales
        matrices = {'A': self.A, 'B': self.B, 'C': self.C}
        # Reemplazar variables por nombres temporales para eval
        expr_eval = expr.replace('A', 'self.A').replace('B', 'self.B').replace('C', 'self.C')
        # Validar suma/resta: todas las matrices involucradas deben tener el mismo shape
        # Extraer todas las matrices involucradas en suma/resta fuera de productos matriciales
        suma_resta = re.split(r'@', expr)
        for bloque in suma_resta:
            # Buscar matrices en el bloque
            mats = re.findall(r'([ABC])', bloque)
            if len(mats) > 1:
                shapes = [matrices[m].shape for m in mats]
                if not all(s == shapes[0] for s in shapes):
                    self.error = f'{{x ∈ Fórmula | dimensiones(x) ≠ {shapes[0]}}}'
                    return False
        # Validar productos matriciales
        productos = re.findall(r'([ABC])@([ABC])', expr)
        for m1, m2 in productos:
            if matrices[m1].shape[1] != matrices[m2].shape[0]:
                self.error = f'{{(A,B) ∈ Fórmula | columnas(A) ≠ filas(B) para producto matricial}}'
                return False
        return True

    def ejecutar_formula(self):
        """
        Ejecuta la fórmula si es válida y guarda el resultado en self.resultado.
        """
        if not self.validar_formula():
            return None
        expr = self.formula.replace('A', 'self.A').replace('B', 'self.B').replace('C', 'self.C')
        try:
            self.resultado = eval(expr)
            return self.resultado
        except Exception as e:
            self.error = f"{{x ∈ Fórmula | error({str(e)})}}"
            return None

    def guardar_resultado_bin(self, filename):
        if self.resultado is not None:
            self.resultado.astype(np.float64).tofile(filename)
        else:
            raise ValueError("No hay resultado para guardar.") 