import numpy as np
import re

from Helpers.utils import logWriter

class MatrizFormula:
    """
    Clase para validar y ejecutar formulas con matrices reales.
    
    Ejemplos de formulas válidas:
        '2*A + 3*B - C'
        '2*C'
        'A - B'
        '3*A'
        
    Ejemplos de formulas inválidas:
        'A*B'
        'A @ B'
'A/B'
'A**2'
'A @ B @ C'
    """
    def __init__(self, A: np.ndarray, B: np.ndarray, C: np.ndarray, formula: str):
        self.A = A
        self.B = B
        self.C = C
        self.formula = formula
        self.resultado = None
        self.error = None

    def validarFormula(self):
        """
        Valida si la formula es correcta segun las reglas permitidas.
        Si no es válida, guarda la justificacion en notacion de conjuntos en self.error.
        """
 
        expr = self.formula.replace(' ', '')
 
        if re.search(r'[^ABC0-9+\-*@().]', expr):
            self.error = '{x ∈ Formula | simbolo no permitido en x}'
            return False
 
        if re.search(r'([ABC])\*([ABC])', expr):
            self.error = '{x ∈ Formula | producto elemento a elemento no permitido}'
            return False
 
        if '/' in expr or '**' in expr:
            self.error = '{x ∈ Formula | operacion no permitida (/, **)}'
            return False
 
        matrices = {'A': self.A, 'B': self.B, 'C': self.C}
 
        exprEval = expr.replace('A', 'self.A').replace('B', 'self.B').replace('C', 'self.C')
 
        sumaResta = re.split(r'@', expr)
        for bloque in sumaResta:
 
            mats = re.findall(r'([ABC])', bloque)
            if len(mats) > 1:
                shapes = []
                for mat in mats:
                    shapes.append(matrices[mat].shape)
                if not all(shape == shapes[0] for shape in shapes):
                    self.error = f'{{x ∈ Formula | dimensiones(x) ≠ {shapes[0]}}}'
                    return False
 
        productos = re.findall(r'([ABC])@([ABC])', expr)
        for m1, m2 in productos:
            mat1Shape = matrices[m1].shape
            mat2Shape = matrices[m2].shape
            if mat1Shape[1] != mat2Shape[0]:
                self.error = f'{{x ∈ Formula | producto matricial incompatible: {mat1Shape} @ {mat2Shape}}}'
                return False
        
        return True

    def ejecutar_formula(self):
        """
        Ejecuta la formula despues de validarla
        """
        if not self.validarFormula():
            return None
        
        try:
            expr = self.formula.replace(' ', '')
            expr = expr.replace('A', 'self.A').replace('B', 'self.B').replace('C', 'self.C')
            resultado = eval(expr)
            self.resultado = resultado
            return resultado
        except Exception as e:
            self.error = f'{{x ∈ Formula | error ejecucion: {str(e)}}}'
            logWriter(f"Error ejecutando formula: {str(e)}", True)
            return None 