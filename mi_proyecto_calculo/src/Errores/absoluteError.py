from error import Error

class AbsoluteError(Error):
    
    def __init__(self, _realValue, _estimatedValue):
        super().__init__( _realValue, _estimatedValue)

    def calculateAE(self):
        absoluteError = abs(self._realValue - self._estimatedValue)
        return absoluteError