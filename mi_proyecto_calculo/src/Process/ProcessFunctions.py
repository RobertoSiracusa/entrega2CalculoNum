import os
import numpy as np
import random

from Helpers.utils import  logWriter, txtWriter
from Repositories.significantFigures import significantFigures
from Repositories.numericSystem import numericSystem
from Repositories.ecuation import Ecuacion
import Repositories.archiveUtil as ArchiveUtil
from Repositories.matrix import Matriz
import numpy as np


def binNumpyArray(binaryContent, dataArray):
    """
    Procesa el contenido binario, lo decodifica y rellena un array NumPy
    sin usar la función 'enumerate'.
    """
    decodedContent = binaryContent.decode('utf-8')
    lineas = decodedContent.splitlines()

    i = 0 
    for linea in lineas:
        elementos = linea.split('#')
        
        j = 0 
        for elemento in elementos:
            
            if i < dataArray.shape[0] and j < dataArray.shape[1]:
                dataArray[i, j] = elemento
            else:
                logWriter(f"Advertencia: Elemento en linea {i}, posicion {j} excede las dimensiones de dataArray. Ignorado.", True)
            j += 1 
        i += 1 

    return dataArray

def initArray(binaryContent):
    decodedContent = binaryContent.decode('utf-8')    

    lineas = decodedContent.splitlines()
    filas = len(lineas)
    maxColumnas = 0
    
    for linea in lineas:

        elementos = linea.split('#')
        numElementos = len(elementos)
        if numElementos > maxColumnas:
            maxColumnas = numElementos

    dataArray = np.full((filas, maxColumnas), "0", dtype='U256')
    
    return dataArray

def initArrayS(filas,col):
   
    dataArray = np.full((filas, col), "0", dtype=np.float64)
    
    return dataArray

def processArray(dataArray):

    for i in range(dataArray.shape[0]):
        for j in range(dataArray.shape[1]):
            value = dataArray[i, j]
            if value == "%z":
                value="0"  
                continue
            try:
                nS = numericSystem(value)
                
                dataArray[i, j] = nS.getNumberBase10()
            except ValueError as e:
                logWriter(f"Error procesando '{value}': {e}",True)
                continue
    return dataArray

def processFormula(matrixAFileName, matrixBFileName):
    pathToFile = "src/Storage"
    archive = ArchiveUtil.ArchiveUtil(pathToFile)
    try:
        with archive.getArchive(matrixAFileName) as fileA, archive.getArchive(matrixBFileName) as fileB:
            binaryContentA = fileA.read()
            binaryContentB = fileB.read()
    except Exception as e:
        logWriter(f"Error al abrir archivos: {e}", True)
        return
    dataArrayA = initArray(binaryContentA)
    dataArrayB = initArray(binaryContentB)

    dataArrayA = binNumpyArray(binaryContentA, dataArrayA)
    dataArrayB = binNumpyArray(binaryContentB, dataArrayB)

    if dataArrayA is None or dataArrayB is None:
        logWriter("Error: Archivos de matriz inválidos", True)
        return
    
    try:
        with open('src/Storage/dataBase_11-09-2021_serial8738.bin', 'r', encoding='utf-8') as f:
            ecuaciones = [linea.strip() for linea in f.readlines()]
    except Exception:
        logWriter("Error: Archivo de ecuaciones invalido", True)
        return
    
    for i, expr in enumerate(ecuaciones[:5], 1):
        ecuacion = Ecuacion(expr)
        resultado = ecuacion.evaluar(dataArrayA, dataArrayB)
        if resultado is None:
            txtWriter("resultados_formulas",f"Ecuacion {i}: No se puede realizar",True)
            continue
        txtWriter("resultados_formulas",f"\nEcuacion {i}: {expr}",True)
        if resultado is None:
            txtWriter("resultados_formulas","No se puede realizar Ecuacion!",True)
        elif isinstance(resultado, Matriz):
            txtWriter("resultados_formulas","Resultado:\n" + str(resultado),True)
        else:
            txtWriter("resultados_formulas","Resultado:\n" + str(resultado),True)

def processMatrix(fileName, pathToFile, filas, columnas):
    archive = ArchiveUtil.ArchiveUtil(pathToFile)
    try:
        with archive.getArchive(fileName) as file:
            binaryContent = file.read()
    except Exception as e:
        logWriter(f"Error al abrir el archivo de matriz {fileName}: {e}", True)
        return None
    
    dataArray = initArrayS(filas, columnas)
    
    decodedContent = binaryContent.decode('utf-8')
    lineas = decodedContent.splitlines()
    
    if len(lineas) < filas:
        logWriter(f"El archivo {fileName} no tiene suficientes filas. Se esperaban {filas}, se encontraron {len(lineas)}", True)
        return None
    
    for i in range(filas):
        elementos = lineas[i].split('#')
        
        if len(elementos) < columnas:
            logWriter(f"La fila {i+1} del archivo {fileName} no tiene suficientes columnas. Se esperaban {columnas}, se encontraron {len(elementos)}", True)
            return None
        
        for j in range(columnas):
            try:
                dataArray[i, j] = float(elementos[j])
            except ValueError as e:
                logWriter(f"Error convirtiendo '{elementos[j]}' a número en {fileName}, fila {i+1}, columna {j+1}: {e}", True)
                return None
    
    return dataArray

def processFormula(fileName, pathToFile):
    """
    Lee fórmulas desde un archivo .bin y las retorna como un array NumPy
    """
    try:
        
        numLineas = 0
        archive = ArchiveUtil.ArchiveUtil(pathToFile)
        
        with archive.getArchive(fileName) as file:
            for line in file:
                numLineas += 1
        
        if numLineas == 0:
            logWriter("El archivo de fórmulas está vacío", True)
            return np.array([], dtype=object)

         
        numpyArray = np.empty(numLineas, dtype=object)
         
     
        archiveReader = ArchiveUtil.ArchiveUtil(pathToFile)
        with archiveReader.getArchive(fileName) as file:
            for i, line in enumerate(file):
         
                if isinstance(line, bytes):
                    numpyArray[i] = line.decode('utf-8').strip()
                else:
                    numpyArray[i] = line.strip()
        
        return numpyArray
    
    except Exception as e:
        logWriter(f"Error al procesar fórmulas: {e}", True)
        return None

def parseMatrixFromFile(filePath):
    """
    Lee una matriz desde un archivo con formato NN#NN#NN o NN#NN#NN#NN
    Toma las últimas 3 líneas válidas del archivo
    Soporta matrices tanto de 3 como de 4 columnas
    """
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
     
        validLines = [line.strip() for line in lines if line.strip()]
        
        if len(validLines) < 3:
            logWriter(f"Error: No hay suficientes líneas válidas en {filePath}", True)
            return None
            
 
        matrixLines = validLines[-3:]
        
        matrix = []
        expectedCols = None
        
        for line in matrixLines:
            row = [float(x) for x in line.split('#')]
            
            # Determina el número de columnas esperado basado en la primera fila
            if expectedCols is None:
                expectedCols = len(row)
                if expectedCols not in [3, 4]:
                    logWriter(f"Error: Número de columnas no soportado en {filePath}: {expectedCols}. Se esperaba 3 o 4", True)
                    return None
            
            # Verifica que todas las filas tengan el mismo número de columnas
            if len(row) == expectedCols:
                matrix.append(row)
            else:
                logWriter(f"Error: Línea con formato incorrecto en {filePath}: {line}. Se esperaban {expectedCols} columnas, se encontraron {len(row)}", True)
                return None
        
        if len(matrix) == 3:
            return np.array(matrix)
        else:
            logWriter(f"Error: No se pudo formar una matriz 3x{expectedCols} completa desde {filePath}", True)
            return None
    except Exception as e:
        logWriter(f"Error leyendo archivo {filePath}: {str(e)}", True)
        return None

def applyGaussJordanToFormulas(numFormulas):
    """
    Aplica Gauss-Jordan a cada archivo de fórmula y escribe los resultados en un único archivo.
    
    Proceso:
    1. Lee cada matriz resultante de las fórmulas (que ya puede ser 3x4)
    2. Si es 3x3, agrega términos independientes aleatorios para crear matriz aumentada 3x4
    3. Si ya es 3x4, la usa directamente como matriz aumentada
    4. Aplica Gauss-Jordan para resolver el sistema de ecuaciones lineales
    5. Extrae las coordenadas de la solución y las guarda
    """
    from Repositories.gaussJordan import GaussJordan
    
    solutions = []
    
    for i in range(1, numFormulas + 1):
        scriptDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        formulaFile = os.path.join(scriptDir, "Storage", f"Formula_{i}.bin.txt")
        
        if os.path.exists(formulaFile):
            
            matrixResult = parseMatrixFromFile(formulaFile)
            
            if matrixResult is not None:
                
                rows, cols = matrixResult.shape
                
                if cols == 3:
                    
                    termsVector = np.array([[random.randint(1, 20)], 
                                          [random.randint(1, 20)], 
                                          [random.randint(1, 20)]])
                    augmentedMatrix = np.hstack([matrixResult, termsVector])
                elif cols == 4:
                    
                    augmentedMatrix = matrixResult
                else:
                    logWriter(f"Error: Matriz de Formula {i} tiene dimensiones incorrectas ({rows}x{cols}). Se esperaba 3x3 o 3x4", True)
                    continue
                
                try:
                    
                    gaussJordan = GaussJordan(augmentedMatrix)
                    solution = gaussJordan.getSolution()
                    
                    
                    lines = solution.strip().split('\n')
                    if len(lines) >= 2:
                        coordinates = lines[1]
                        solutions.append(coordinates)
                    
                except Exception as e:
                    logWriter(f"Error aplicando Gauss-Jordan a Fórmula {i}: {str(e)}", True)
 
            else:
                logWriter(f"No se pudo leer la matriz de la Fórmula {i}", True)
 
        else:
            logWriter(f"Error:Formula Invalida {i}", True)
    
    writeGaussJordanResults(solutions)

def writeGaussJordanResults(solutions):
    """
    Escribe las soluciones de Gauss-Jordan en un único archivo GaussJordan.txt
    """
    try:
        scriptDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storagePath = os.path.join(scriptDir, "Storage")
        filePath = os.path.join(storagePath, "GaussJordan.txt")
        
 
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write("Soluciones de los sistemas de ecuaciones:\n")
            for solution in solutions:
                file.write(f"{solution}\n")
                
    except Exception as e:
        logWriter(f"Error escribiendo archivo GaussJordan.txt: {str(e)}", True)
