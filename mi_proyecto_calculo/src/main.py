

from Helpers.utils import logWriter

import Process.ProcessFunctions as pf
import Repositories.archiveUtil as ArchiveUtil
import Composables.storeNumbers as storeNumbers
from Repositories.matrixElementalOperation import MatrixOperations

def main():
    pathToFile = "mi_proyecto_calculo/src/Storage"
    arrayFile1 = 'valoresNumerosBases.bin'
    
    try:
        archive = ArchiveUtil.ArchiveUtil(pathToFile)
        
        with archive.getArchive(arrayFile1) as file:
            binaryContent = file.read()  
    
        dataArrayN1 = pf.initArray(binaryContent)
       
        dataArrayN1 = pf.binNumpyArray(binaryContent, dataArrayN1)
        
        storeNumbers.storeSignificantFigures(dataArrayN1)
        
        dataArrayN1 = pf.processArray(dataArrayN1)
        print("AAA")
        storeNumbers.storeGaussJordan(dataArrayN1)
        print("BBB")
        archive=None
        dataArrayN1=None
        
    except Exception as e:
        logWriter("Error al procesar archivo: " + str(e), True)
        
main()
