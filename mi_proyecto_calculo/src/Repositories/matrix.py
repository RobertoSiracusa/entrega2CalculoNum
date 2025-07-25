class Matriz:
    def __init__(self, datos):
        self.datos = datos
        self.dimension = len(datos)
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, fila)) for fila in self.datos])
    
    def __add__(self, otra):
        if isinstance(otra, Matriz):
            if self.dimension != otra.dimension:
                raise ValueError("Dimensiones incompatibles")
            resultado = []
            for i in range(self.dimension):
                fila = [self.datos[i][j] + otra.datos[i][j] for j in range(self.dimension)]
                resultado.append(fila)
            return Matriz(resultado)
        elif isinstance(otra, int):
            resultado = [[self.datos[i][j] + otra for j in range(self.dimension)] for i in range(self.dimension)]
            return Matriz(resultado)
        raise TypeError("Tipo no soportado")
    
    def __sub__(self, otra):
        if isinstance(otra, Matriz):
            if self.dimension != otra.dimension:
                raise ValueError("Dimensiones incompatibles")
            resultado = []
            for i in range(self.dimension):
                fila = [self.datos[i][j] - otra.datos[i][j] for j in range(self.dimension)]
                resultado.append(fila)
            return Matriz(resultado)
        elif isinstance(otra, int):
            resultado = [[self.datos[i][j] - otra for j in range(self.dimension)] for i in range(self.dimension)]
            return Matriz(resultado)
        raise TypeError("Tipo no soportado")
    
    def __mul__(self, otra):
        if isinstance(otra, Matriz):
            if self.dimension != otra.dimension:
                raise ValueError("Dimensiones incompatibles")
            resultado = [[0]*self.dimension for _ in range(self.dimension)]
            for i in range(self.dimension):
                for j in range(self.dimension):
                    for k in range(self.dimension):
                        resultado[i][j] += self.datos[i][k] * otra.datos[k][j]
            return Matriz(resultado)
        elif isinstance(otra, int):
            resultado = [[self.datos[i][j] * otra for j in range(self.dimension)] for i in range(self.dimension)]
            return Matriz(resultado)
        raise TypeError("Tipo no soportado")
    
    def __rmul__(self, escalar):
        return self * escalar
    
    def __rsub__(self, escalar):
        resultado = [[escalar - self.datos[i][j] for j in range(self.dimension)] for i in range(self.dimension)]
        return Matriz(resultado)
    
    def __radd__(self, escalar):
        return self + escalar