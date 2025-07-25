import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Helpers.utils import logWriter

class GaussSeidelSolver:
    def __init__(self, augmentedMatrix: np.ndarray, tol=1e-10, maxIter=1000):
        if not isinstance(augmentedMatrix, np.ndarray):
            errorMsg = "El parametro 'augmentedMatrix' debe ser un array de NumPy (np.ndarray)."
            logWriter(errorMsg, True)
            return
        
        if augmentedMatrix.ndim != 2:
            errorMsg = "La matriz aumentada debe ser bidimensional (Ejemplo: forma (filas, columnas))."
            logWriter(errorMsg, True)
            return

        if augmentedMatrix.size == 0 or augmentedMatrix.shape[0] == 0:
            errorMsg = "La matriz aumentada no debe estar vacia (debe tener al menos una fila)."
            logWriter(errorMsg, True)
            return

        if augmentedMatrix.shape[1] < 2:
            errorMsg = "La matriz aumentada debe tener al menos 2 columnas (matriz de coeficientes A y vector de términos independientes b)."
            logWriter(errorMsg, True)
            return

        
        self.augmentedMatrix = augmentedMatrix.astype(float)
        self.nRows, self.nCols = self.augmentedMatrix.shape
        
        
        self.matrixA = self.augmentedMatrix[:, :-1]
        self.vectorB = self.augmentedMatrix[:, -1]
        
       
        self.tolerance = tol
        self.maxIterations = maxIter
        
        
        self.x = None
        self.y = None
        self.z = None
        self.solutionStringsDict = {} 
        self.rawSolutionValues = None
        self.finalSolution = "No resuelto"
        
        
        self.iterations = 0
        self.converged = False
        self.iterationHistory = None
        self.initialGuess = None
        
        
        self._validateMatrix()
        
        
        if self.nRows > self.nCols - 1:
            errorMsg = "El sistema puede estar sobredeterminado o no tener solucion unica."
            logWriter(errorMsg, True)
            
        if self.nRows < self.nCols - 1:
            errorMsg = "El sistema puede tener infinitas soluciones o ser indeterminado."
            logWriter(errorMsg, True)
            

        np.set_printoptions(precision=4, suppress=False)

    def _validateMatrix(self):
        """Validacion especifica para Gauss-Seidel"""
        if self.matrixA.shape[0] != self.matrixA.shape[1]:
            errorMsg = "La matriz de coeficientes A debe ser cuadrada para Gauss-Seidel."
            logWriter(errorMsg, True)
            return
        
        
        for i in range(self.nRows):
            if abs(self.matrixA[i, i]) < 1e-15:
                errorMsg = f"El elemento diagonal A[{i},{i}] es cero o casi cero. La iteracion podria no converger."
                logWriter(errorMsg, True)
                return
        
        
        if self.vectorB.shape[0] != self.nRows:
            errorMsg = f"El vector b debe tener {self.nRows} elementos, pero tiene {self.vectorB.shape[0]}."
            logWriter(errorMsg, True)
            return

    def _checkDiagonalDominance(self) -> bool:
        """Verifica si la matriz es diagonalmente dominante (condicion suficiente para convergencia)"""
        for i in range(self.nRows):
            diagonalElement = abs(self.matrixA[i, i])
            sumOffDiagonal = np.sum(np.abs(self.matrixA[i, :])) - diagonalElement
            
            if diagonalElement <= sumOffDiagonal:
                return False
        return True

    def resolveSystem(self, initialGuess: np.ndarray = None, saveHistory: bool = False) -> np.ndarray:
        """Resolver el sistema usando Gauss-Seidel"""
        
        
        self.x = "No resuelto"
        self.y = "No resuelto"
        self.z = "No resuelto"
        self.solutionStringsDict = {}
        self.rawSolutionValues = None
        self.iterations = 0
        self.converged = False
        
       
        if initialGuess is None:
            currentSolution = np.zeros(self.nRows, dtype=float)
        else:
            if initialGuess.shape[0] != self.nRows:
                errorMsg = f"El vector inicial debe tener {self.nRows} elementos, pero tiene {initialGuess.shape[0]}."
                logWriter(errorMsg, True)
                return None
            currentSolution = np.array(initialGuess, dtype=float)
        
        self.initialGuess = currentSolution.copy()
        
        
        if not self._checkDiagonalDominance():
            warningMsg = "Advertencia: La matriz no es diagonalmente dominante. La convergencia no esta garantizada."
            logWriter(warningMsg, True)
            
        
        
        if saveHistory:
            historySize = min(self.maxIterations + 1, 10000)  # Limitar memoria
            self.iterationHistory = np.zeros((historySize, self.nRows), dtype=float)
            self.iterationHistory[0, :] = currentSolution.copy()
        
        
        
       
        for iteration in range(1, self.maxIterations + 1):
            previousSolution = currentSolution.copy()
            
            
            for i in range(self.nRows):
                
                sumPrevious = 0.0
                for j in range(i):
                    sumPrevious += self.matrixA[i, j] * currentSolution[j]
                
                
                sumNext = 0.0
                for j in range(i + 1, self.nRows):
                    sumNext += self.matrixA[i, j] * previousSolution[j]
                
                
                currentSolution[i] = (self.vectorB[i] - sumPrevious - sumNext) / self.matrixA[i, i]
            
            
            if saveHistory and iteration < historySize:
                self.iterationHistory[iteration, :] = currentSolution.copy()
            
            
            if np.allclose(previousSolution, currentSolution, rtol=self.tolerance, atol=self.tolerance):
                
                self.iterations = iteration
                self.converged = True
                break
            
            self.iterations = iteration
        
        if not self.converged:
            warningMsg = f"No convergio dentro de {self.maxIterations} iteraciones."
            logWriter(warningMsg, True)
            
        
        
        self.rawSolutionValues = currentSolution.copy()
        self._formatSolution()
        logWriter("Matriz verificada con Seidel correctamente.", True)
        
        return currentSolution.copy()

    def _formatSolution(self):
        """Formatear la solucion siguiendo la estructura de GaussJordan"""
        if self.rawSolutionValues is None:
            return
        
        solutionValues = self.rawSolutionValues
        
        if len(solutionValues) >= 3:
            self.x = f"x = {solutionValues[0]:.6f}"
            self.y = f"y = {solutionValues[1]:.6f}"
            self.z = f"z = {solutionValues[2]:.6f}"
            
            self.solutionStringsDict['x'] = self.x
            self.solutionStringsDict['y'] = self.y
            self.solutionStringsDict['z'] = self.z

            convergenceStatus = "Convergido" if self.converged else "No convergido"
            self.finalSolution = (
                f"Solucion del sistema de ecuaciones (Gauss-Seidel):\n"
                f"{self.x}, {self.y}, {self.z}\n"
                f"Iteraciones: {self.iterations}\n"
                f"Estado: {convergenceStatus}"
            )
        elif len(solutionValues) >= 2:
            self.x = f"x = {solutionValues[0]:.6f}"
            self.y = f"y = {solutionValues[1]:.6f}"
            self.z = "No aplicable (sistema 2x2)"
            
            self.solutionStringsDict['x'] = self.x
            self.solutionStringsDict['y'] = self.y

            convergenceStatus = "Convergido" if self.converged else "No convergido"
            self.finalSolution = (
                f"Solucion del sistema de ecuaciones (Gauss-Seidel):\n"
                f"{self.x}, {self.y}\n"
                f"Iteraciones: {self.iterations}\n"
                f"Estado: {convergenceStatus}"
            )
            
        else:
            self.x = "No aplicable (menos de 2 variables)"
            self.y = "No aplicable (menos de 2 variables)"
            self.z = "No aplicable (menos de 2 variables)"
            self.solutionStringsDict.clear()
            self.finalSolution = "Solucion: No hay suficientes variables para mostrar x, y, z"
    def getSolutionStrings(self) -> dict:
        """Obtener las soluciones formateadas como un diccionario"""
        return self.solutionStringsDict

    def getSolution(self) -> str:
        """Obtener la solucion formateada (compatible con GaussJordan)"""
        if self.finalSolution == "No resuelto":
            return "El sistema no ha sido resuelto."
        return self.finalSolution

    def getRawSolution(self) -> np.ndarray:
        """Obtener la solucion como array numpy"""
        if self.rawSolutionValues is None:
            errorMsg = "El sistema no ha sido resuelto aun."
            logWriter(errorMsg, True)
            return None
        return self.rawSolutionValues.copy()

    def getIterations(self) -> int:
        """Obtener numero de iteraciones realizadas"""
        return self.iterations

    def isConverged(self) -> bool:
        """Verificar si el método convergio"""
        return self.converged

    def getIterationHistory(self) -> np.ndarray:
        """Obtener historial de iteraciones (si se guardo)"""
        if self.iterationHistory is None:
            errorMsg = "No se guardo historial. Use saveHistory=True en resolveSystem()."
            logWriter(errorMsg, True)
            return None
        
        # Retornar solo las iteraciones validas
        validIterations = self.iterations + 1 if self.iterations > 0 else 1
        return self.iterationHistory[:validIterations, :].copy()

    

    def verifyMatrix(self) -> bool:
        
        
        
        isDiagonalDominant = self._checkDiagonalDominance()
        
        
        
        
        
        return isDiagonalDominant 