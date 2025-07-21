import datetime
import random

from Repositories.significantFigures import significantFigures
from Repositories.numericSystem import numericSystem
from Helpers.utils import logWriter, txtWriter
from Repositories.elementalOperation import elementalOperation
from Repositories.gaussJordan import GaussJordan

def storeSignificantFigures(dataArray):

    currentDateTime = datetime.datetime.now()
    formattedDateTime = currentDateTime.strftime("%Y-%m-%d_%H-%M-%S")
    randNum = random.randint(1, 100)
    outputFileName = f"InformaciónNumérica_{formattedDateTime}_serial{randNum}"
    

    

    for i in range(dataArray.shape[0]):
        for j in range(dataArray.shape[1]):
            value = dataArray[i, j]
            if value == "%z":  
                continue
            try:
                
                sf = significantFigures(value)
                nS = numericSystem(value)
                eO = elementalOperation(value, nS.binSystem, nS.decSystem, nS.hexSystem)
                

                text= sf.toString()+"\n"+nS.toString()+"\n"+eO.toString()+"\n"+"Numero en Base 10:"+str(nS.getNumberBase10())+"\n"
                txtWriter(outputFileName,text,True)
            except ValueError as e:
                logWriter(f"Error procesando '{value}': {e}",True)
                continue

def storeGaussJordan(dataArray):
    currentDateTime = datetime.datetime.now()
    formattedDateTime = currentDateTime.strftime("%Y-%m-%d_%H-%M-%S")
    randNum = random.randint(1, 100)
    outputFileName = f"GaussJordan_{formattedDateTime}_serial{randNum}"
    
    try:
        gJ = GaussJordan(dataArray)
        txtWriter(outputFileName, gJ.getSolution(), True)
    except Exception as e:
        logWriter(f"Error en Gauss-Jordan: {e}",True)