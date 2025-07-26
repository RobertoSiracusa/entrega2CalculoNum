

import os
import numpy as np
from Helpers.utils import logWriter
from Helpers.dataGenerator import generateRandomMatrixFiles
from Helpers.distanceCalculator import generateDistanceReport

import Process.ProcessFunctions as pf
import Repositories.archiveUtil as ArchiveUtil
import Composables.storeNumbers as storeNumbers
from Repositories.matrixElementalOperation import MatrixOperations
from Repositories.matrizFormula import MatrizFormula

def main():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    pathToFile = os.path.join(scriptDir, "Storage")
    

    if not generateRandomMatrixFiles():
        logWriter("Error: No se pudieron generar los archivos de matrices", True)
        return
    
    arrayFile1 = 'valoresNumerosBases.bin'
    matrixAFileName="randomFile1.bin"
    matrixBFileName="randomFile2.bin"
    matrixCFileName="randomFile3.bin"
    formulasFileName="formulasMarrugo.bin"
    matrixA=None
    matrixB=None
    matrixC=None
    arrayFormulas=None
    
    try:
        archiveRandomsNumbers = ArchiveUtil.ArchiveUtil(pathToFile)
        
        with archiveRandomsNumbers.getArchive(arrayFile1) as file:
            binaryContent = file.read()  
    
        dataArrayN1 = pf.initArray(binaryContent)
       
        dataArrayN1 = pf.binNumpyArray(binaryContent, dataArrayN1)
    
        storeNumbers.storeSignificantFigures(dataArrayN1)
        
        matrixA=pf.processMatrix(matrixAFileName,pathToFile,3,4)
        matrixB=pf.processMatrix(matrixBFileName,pathToFile,3,4)
        matrixC=pf.processMatrix(matrixCFileName,pathToFile,3,4)


        arrayFormulas=pf.processFormula(formulasFileName,pathToFile)
        

        if arrayFormulas is None or len(arrayFormulas) == 0:
            logWriter("Error: No se pudieron cargar las fórmulas desde el archivo", True)
            return
        

        for i in range(len(arrayFormulas)):
            elemento=str(arrayFormulas[i])
        
            try:
                mf = MatrizFormula(matrixA, matrixB, matrixC, elemento)

                resultado = mf.ejecutar_formula()
                
                if hasattr(mf, 'error') and mf.error:
                    logWriter(f"Error:Formula Invalida {i+1}", True)
                elif resultado is not None:
                    storeNumbers.storeMatrix(resultado,"Formula_"+str((i+1))+".bin")
                else:
                    logWriter(f"Error:Formula Invalida {i+1}", True)
                    
            except Exception as e:
                logWriter(f"Error:Formula Invalida {i+1}", True)
        

        pf.applyGaussJordanToFormulas(len(arrayFormulas))
        

        if not generateDistanceReport():
            logWriter("Error: No se pudo generar el reporte de distancias", True)
        
        archive=None
        dataArrayN1=None
        
    except Exception as e:
        logWriter("Error al procesar archivo: " + str(e), True)
        
main()
