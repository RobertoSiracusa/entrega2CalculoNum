import numpy as np

from Helpers.utils import  logWriter, txtWriter
from Repositories.significantFigures import significantFigures
from Repositories.numericSystem import numericSystem
from Repositories.ecuation import Ecuacion
import Repositories.archiveUtil as ArchiveUtil
from Repositories.matrix import Matriz


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
                logWriter(f"Advertencia: Elemento en línea {i}, posición {j} excede las dimensiones de dataArray. Ignorado.", False)
            j += 1 
        i += 1 

    return dataArray

def initArray(binaryContent):
    decodedContent = binaryContent.decode('utf-8')    

    lineas = decodedContent.splitlines()
    filas = len(lineas)
    max_columnas = 0
    
    for linea in lineas:

        elementos = linea.split('#')
        num_elementos = len(elementos)
        if num_elementos > max_columnas:
            max_columnas = num_elementos

    dataArray = np.full((filas, max_columnas), "0", dtype='U256')
    
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
            binary_content_A = fileA.read()
            binary_content_B = fileB.read()
    except Exception as e:
        logWriter(f"Error al abrir archivos: {e}", True)
        return
    dataArrayA = initArray(binary_content_A)
    dataArrayB = initArray(binary_content_B)

    dataArrayA = binNumpyArray(binary_content_A, dataArrayA)
    dataArrayB = binNumpyArray(binary_content_B, dataArrayB)

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
