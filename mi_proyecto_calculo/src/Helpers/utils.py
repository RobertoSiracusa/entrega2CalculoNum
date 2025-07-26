import os
import numpy as np
import Repositories.archiveUtil as ArchiveUtil 
import random
import datetime

def logWriter(content, appendNewLine):
    scriptDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pathToFile = os.path.join(scriptDir, "Storage")
    archive = ArchiveUtil.ArchiveUtil(pathToFile)

    currentDateTime = datetime.datetime.now()
    formattedDateTime = currentDateTime.strftime("%Y-%m-%d_%H-%M-%S")
    randNum = random.randint(1, 99)
    outputLogFileName = f"ErrorLog[{formattedDateTime}_serial{randNum}]:"
    logFileName="ErrorReport"

    archive.setCreateArchiveLog(content,logFileName,outputLogFileName,appendNewLine)

def txtWriter(outputFileName, content, appendNewLine=True):
    scriptDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pathToFile = os.path.join(scriptDir, "Storage")
    archive = ArchiveUtil.ArchiveUtil(pathToFile)

    archive.setCreateArchiveTxt(content, outputFileName, appendNewLine)

def format2DArray(inputArray: np.ndarray) -> str:
        
        if not isinstance(inputArray, np.ndarray):
            return "Error: La entrada no es un array de numpy."
        if inputArray.ndim != 2:
            return "Error: El array debe ser de dos dimensiones."
        if inputArray.shape[0] > 3 or inputArray.shape[1] > 4:
            return "Error: El array excede las dimensiones máximas permitidas (3x4)."

        outputString = ""
        for rowIdx in range(inputArray.shape[0]):
            for colIdx in range(inputArray.shape[1]):
                item = inputArray[rowIdx, colIdx]
                try:
                    num = int(item)
                    outputString += f"{num:02d}"
                except ValueError:
                    return f"Error: El contenido del array debe ser convertible a número. Valor inválido: '{item}'"

                if colIdx < inputArray.shape[1] - 1:
                    outputString += "#"
            if rowIdx < inputArray.shape[0] - 1:
                outputString += "\n"
        return outputString
