import numpy as np

from Helpers.utils import logWriter

class GaussJordan:
    def __init__(self, augmentedMatrix: np.ndarray):  
        if not isinstance(augmentedMatrix, np.ndarray):
            errorMsg = "El parámetro 'augmentedMatrix' debe ser un array de NumPy (np.ndarray)."
            logWriter( errorMsg,True)
        
        if augmentedMatrix.ndim != 2:
            errorMsg = "La matriz aumentada debe ser bidimensional (Ejemplo: forma (filas, columnas))."
            logWriter( errorMsg,True)


        if augmentedMatrix.size == 0 or augmentedMatrix.shape[0] == 0:
            errorMsg = "La matriz aumentada no debe estar vacía (debe tener al menos una fila)."
            logWriter( errorMsg,True)


        if augmentedMatrix.shape[1] < 2:
            errorMsg = "La matriz aumentada debe tener al menos 2 columnas (matriz de coeficientes A y vector de términos independientes b)."
            logWriter( errorMsg,True)

        self.augmentedMatrix = augmentedMatrix.astype(float)
        self.nRows, self.nCols = self.augmentedMatrix.shape
        self.x = None
        self.y = None
        self.z = None
        self.solutionStringsDict = {} 
        self.rawSolutionValues = None
        self.finalSolution = "No resuelto"
        self.resolveMatrix()

        # Advertencias sobre el tamaño del sistema
        if self.nRows > self.nCols - 1:
            errorMsg = "El sistema puede estar sobredeterminado o no tener solucion unica."
            logWriter(errorMsg,True)
            print(errorMsg)
        if self.nRows < self.nCols - 1:
            errorMsg = "El sistema puede tener infinitas soluciones o ser indeterminado."
            logWriter(errorMsg,True)
            

        np.set_printoptions(precision=4, suppress=False)

    def swapRows(self, matrix: np.ndarray, row1: int, row2: int):
        matrix[[row1, row2]] = matrix[[row2, row1]]

    def swapColumns(self, matrix: np.ndarray, col1: int, col2: int):
        matrix[:, [col1, col2]] = matrix[:, [col2, col1]]

    def partialPivoting(self, matrix: np.ndarray, k: int) -> np.ndarray:
        n = matrix.shape[0]
        maxIndex = k + np.argmax(np.abs(matrix[k:, k]))

        if maxIndex != k:
            self.swapRows(matrix, k, maxIndex)
        return matrix

    def completePivoting(self, matrix: np.ndarray, k: int) -> tuple[np.ndarray, list]:
        n, m = matrix.shape
        submatrix = np.abs(matrix[k:n, k:m-1])

        if submatrix.size == 0: 
            return matrix, []
        
        maxFlatIndex = np.argmax(submatrix)
        rowIndexOffset, colIndexOffset = np.unravel_index(maxFlatIndex, submatrix.shape)

        pivotRow = k + rowIndexOffset
        pivotCol = k + colIndexOffset

        swappedColumns = []

        if pivotRow != k:
            self.swapRows(matrix, k, pivotRow)

        if pivotCol != k:
            self.swapColumns(matrix, k, pivotCol)
            swappedColumns.append((k, pivotCol))
        return matrix, swappedColumns

    def scaledPivoting(self, augmentedMatrix: np.ndarray, k: int) -> np.ndarray:
        n, m = augmentedMatrix.shape
        scaleFactors = np.zeros(n)

        for i in range(n):
            if augmentedMatrix[i, :m-1].size > 0:
                scaleFactors[i] = np.max(np.abs(augmentedMatrix[i, :m-1]))
            else:
                scaleFactors[i] = 0.0 

        maxRatio = -1.0
        rowWithMaxRatio = k

        for i in range(k, n):
            if scaleFactors[i] == 0:
                ratio = 0.0
            else:
                ratio = np.abs(augmentedMatrix[i, k]) / scaleFactors[i]

            if ratio > maxRatio:
                maxRatio = ratio
                rowWithMaxRatio = i
        if rowWithMaxRatio != k:
            self.swapRows(augmentedMatrix, k, rowWithMaxRatio)
        return augmentedMatrix

    def resolveMatrix(self, pivotingType: str = "parcial") -> np.ndarray | None:

        currentMatrix = self.augmentedMatrix
        
        self.x = "No resuelto"
        self.y = "No resuelto"
        self.z = "No resuelto"
        self.solutionStringsDict = {} 
        self.rawSolutionValues = None

        originalColumnOrder = np.arange(self.nCols - 1) if pivotingType == "full" else None

        for k in range(self.nRows):
            if pivotingType == "parcial":
                currentMatrix = self.partialPivoting(currentMatrix, k)
            elif pivotingType == "completo": 
                currentMatrix, swaps = self.completePivoting(currentMatrix, k)
                if originalColumnOrder is not None: 
                    for col1Idx, col2Idx in swaps:
                        originalColumnOrder[[col1Idx, col2Idx]] = originalColumnOrder[[col2Idx, col1Idx]]
            elif pivotingType == "escalonado":
                currentMatrix = self.scaledPivoting(currentMatrix, k)
            elif pivotingType != "none":
                errorMsg = f"Tipo de pivoteo '{pivotingType}' no reconocido. No se aplicara el pivoteo"
                logWriter(errorMsg,True)

            pivot = currentMatrix[k, k]

            if abs(pivot) < 1e-9: 
                errorMsg = f"Error: Pivote igual a cero o casi cero en la fila {k} despues del pivoteo. El sistema podria no tener una solucion unica o ser inconsistente."
                logWriter(errorMsg,True)

            currentMatrix[k, :] = currentMatrix[k, :] / pivot

            for i in range(self.nRows):
                if i != k:
                    factor = currentMatrix[i, k]
                    currentMatrix[i, :] = currentMatrix[i, :] - factor * currentMatrix[k, :]

        solutionValues = None

        if pivotingType == "completo" and originalColumnOrder is not None: 
            unorderedSolution = currentMatrix[:, -1]
            solutionValues = np.zeros_like(unorderedSolution)
            for i, originalIdx in enumerate(originalColumnOrder):
                solutionValues[originalIdx] = unorderedSolution[i]
        else:
            solutionValues = currentMatrix[:, -1]
        
        self.rawSolutionValues = solutionValues

        if len(solutionValues) >= 3:
            self.x = f"x = {solutionValues[0]:.6f}"
            self.y = f"y = {solutionValues[1]:.6f}"
            self.z = f"z = {solutionValues[2]:.6f}"
            
            self.solutionStringsDict['x'] = self.x
            self.solutionStringsDict['y'] = self.y
            self.solutionStringsDict['z'] = self.z

            finalSolutionForTxt = (
                f"Solucion del sistema de ecuaciones:\n"
                f"{self.x}, "
                f"{self.y}, "
                f"{self.z}"
            )
        else:
            self.x = "No aplicable (menos de 3 vars)"
            self.y = "No aplicable (menos de 3 vars)"
            self.z = "No aplicable (menos de 3 vars)"
            self.solutionStringsDict.clear()
            finalSolutionForTxt = "Solucion: No hay suficientes variables (se esperaban 3 para x, y, z)"

        self.finalSolution = finalSolutionForTxt
        
        return currentMatrix
    
    def getSolution(self) -> str:
        if self.finalSolution == "No resuelto":
            return "El sistema no ha sido resuelto."
        return self.finalSolution
