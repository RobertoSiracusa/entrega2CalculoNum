
import os
import sys
import random


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Helpers.DataGenerate import archiveGenerator

def generateRandomMatrixFiles():
    
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
    
 
    matrix = []
    for i in range(3):
        row = []
        
        for j in range(3):
            row.append(random.randint(-30, 30))
        
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
    
    success = generateRandomMatrixFiles()
    if success:
        print("Archivos generados exitosamente")
    else:
        print("Error generando archivos")

if __name__ == "__main__":
    main()