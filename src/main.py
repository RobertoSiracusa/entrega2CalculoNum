

from Helpers.utils import logWriter

import Process.ProcessFunctions as pf
import Repositories.archiveUtil as ArchiveUtil
import Composables.storeNumbers as storeNumbers
from Repositories.matrixElementalOperation import MatrixOperations

def main():
    pathToFile = "src/Storage"
    arrayFile1 = 'resultValues_20-05-2025_serial1989.bin'
    

    try:
        archive = ArchiveUtil.ArchiveUtil(pathToFile)
        
        with archive.getArchive(arrayFile1) as file:
            binary_content = file.read()  
            
        dataArrayN1 = pf.initArray(binary_content)
       
         
        dataArrayN1 = pf.binNumpyArray(binary_content, dataArrayN1)
        storeNumbers.storeSignificantFigures(dataArrayN1)

        dataArrayN1 = pf.processArray(dataArrayN1)

        matrixChecker = MatrixOperations(dataArrayN1)
        
        storeNumbers.storeGaussJordan(dataArrayN1)
        pf.processFormula("matrizA.bin", "matrizB.bin")
        archive=None
        dataArray1=None
        
    except Exception as e:
        logWriter("Error al procesar archivo: " + str(e), True)
        
main()
