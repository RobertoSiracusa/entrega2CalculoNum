from error import Error 
from absoluteError import AbsoluteError
from roundingError import RoundingError
from truncationError import TruncationError
from propagationError import PropagationError
from relativeError import RelativeError

obj = Error(123.456789,123.446789)
objAE = AbsoluteError(obj.getRealValue(), obj.getEstimatedValue())
objRE = RelativeError(obj.getRealValue(), obj.getEstimatedValue())
objRndE = RoundingError(obj.getRealValue())
objTE  = TruncationError(0.5,3)
objPropE = PropagationError(1.0)

print("Error Absoluto: ", objAE.calculateAE())
print("Error Relativo: ", objRE.calculateRE())
print("Error Redondeo: ", objRndE.calculateRndE())
print("Error Truncamiento: ", objTE.calculateTE())
print("Error Propagacion: ", objPropE.calculatePropE())