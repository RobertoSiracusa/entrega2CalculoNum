class Error:
    _realValue = 0
    _estimatedValue = 0

    def __init__(self,_realValue,_estimatedValue):
        self._realValue = self.__verify(_realValue)
        self._estimatedValue =  self.__verify(_estimatedValue)

    
    def getRealValue(self):
        return self._realValue
    
    def setRealValue(self,_realValue):
        self._realValue = self.__verify(_realValue)
    
    def getEstimatedValue(self):
        return self._estimatedValue

    def setEstimatedValue(self,_estimatedValue):
        self._estimatedValue = self.__verify(_estimatedValue)

    def __verify(self, valueToCheck):
        if valueToCheck == None:
            raise ValueError("El valor no puede ser nulo.")
        if self.__isNumber(valueToCheck):
            return valueToCheck
        else:
            raise TypeError("El valor debe ser un número (entero o flotante).")
    
    def __isNumber(self, valueToCheck):
        tipo = type(valueToCheck)
        if tipo == int or tipo == float:
            return True
        else:
            return False