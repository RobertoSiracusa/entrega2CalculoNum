from absoluteError import AbsoluteError
from math import factorial, cos

class TruncationError(AbsoluteError):
   
    def __init__(self,valueToAprox=0.5,nTerms=3):
        _realValue = cos(valueToAprox)
        _truncatedValue = self.__aproximateFunction(valueToAprox, nTerms)
        super().__init__(_realValue, _truncatedValue)

    def calculateTE(self):
        return super().calculateAE()

    def __aproximateFunction(self,valueToAprox,nTerms):
        suma = 0
        for i in range(nTerms):
            suma += (-1)**i * (valueToAprox**(2*i)) / factorial(2*i)
        return suma