class Ecuacion:
    def __init__(self, expresion):
        self.expresion = expresion
    
    def evaluar(self, matrizA, matrizB):
        try:
            expr = self.expresion.replace('[', '').replace(']', '')
            return eval(expr, {'A': matrizA, 'B': matrizB})
        except Exception:
            return None

def leerMatriz(nombreArchivo):
    try:
        with open(nombreArchivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        datos = []
        for linea in lineas:
            linea = linea.strip()
            if linea:
                numeros = [int(x) for x in linea.split('#')]
                datos.append(numeros)
        return Matriz(datos)
    except Exception:
        return None