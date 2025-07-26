
import os
import sys
import random


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Helpers.DataGenerate import archiveGenerator

def generateRandomMatrixFiles():
    """
    Genera los archivos randomFile1.bin, randomFile2.bin, randomFile3.bin 
    con matrices aumentadas 3x4 de números aleatorios usando el formato correcto (#)
    Las matrices A, B, C son directamente 3x4 (matriz aumentada para Gauss-Jordan)
    """
    scriptDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storagePath = os.path.join(scriptDir, "Storage")
    
    try:
    
        for i in range(3):
            fileName = f"randomFile{i+1}.bin"
            generateMatrixFile(storagePath, fileName)
            
        return True
        
    except Exception as e:
        return False

def generateMatrixFile(storagePath, fileName):
    """
    Genera un archivo con matriz aumentada 3x4 usando formato #
    Las primeras 3 columnas son la matriz de coeficientes (A)
    La cuarta columna son los términos independientes (b)
    Esto crea directamente una matriz aumentada [A|b]
    """
 
    matrix = []
    for i in range(3):
        row = []
        # Primeras 3 columnas: matriz de coeficientes
        for j in range(3):
            row.append(random.randint(-30, 30))
        # Cuarta columna: términos independientes
        row.append(random.randint(1, 50))
        matrix.append(row)
    
 
    filePath = os.path.join(storagePath, fileName)
    
    try:
        with open(filePath, 'w', encoding='utf-8') as file:
            for i, row in enumerate(matrix):
                rowStr = '#'.join(map(str, row))
                file.write(rowStr)
                if i < len(matrix) - 1:
                    file.write('\n')
        
        return True
        
    except Exception as e:
        return False

def main():
    """
    Función principal para probar la generación de archivos
    """
    success = generateRandomMatrixFiles()
    if success:
        print("Archivos generados exitosamente")
    else:
        print("Error generando archivos")

if __name__ == "__main__":
    main()