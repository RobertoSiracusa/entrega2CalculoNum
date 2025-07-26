from absoluteError import AbsoluteError

class PropagationError(AbsoluteError):
    def __init__(self, initialValue = 1.0):
        self.initialValue = initialValue
        __realResult = (self.initialValue * 3)
        __errorResult = self.__resultWhitError()
        super().__init__(__realResult, __errorResult)

    def __resultWhitError(self):
        return ((self.initialValue * 0.1)*3 - 0.3 )
    
    def calculatePropE(self):
        return super().calculateAE()