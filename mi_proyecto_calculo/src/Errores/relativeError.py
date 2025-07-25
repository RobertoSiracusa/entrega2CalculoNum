from absoluteError import AbsoluteError

class RelativeError(AbsoluteError):

    def __init__(self, realValue, estimatedValue):
        super().__init__(realValue, estimatedValue)

    def calculateRE(self):
        AE = self.calculateAE()
        if self._realValue == 0:
            raise ValueError("El valor real no puede ser cero para calcular el error relativo.")
        else:
            relativeError = AE / abs(self._realValue)
            return relativeError
        
    def porcentualRE(self):
        return (self.calculateRE() * 100)