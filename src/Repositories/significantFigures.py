class significantFigures:

    def __init__(self, number):
        self.number = str(number.strip())
        self.significantFigures = None
        self.normalizedForm = None  
        
        self.checkDecimalSystem()
       
        self.calculateNormalizedForm()
    
    def checkDecimalSystem(self):
        
        cleanNumber = self.number
        if cleanNumber.startswith('-') or cleanNumber.startswith('+'):
            cleanNumber = cleanNumber[1:]
        
        dotFound = False
        for char in cleanNumber:
            if char== ',':
                
                char = '.'
            if char == '.':
                if dotFound:  
                    self.setSignificantFigures("Sistema Numerico Invalido")
                    return
                dotFound = True
            elif not char.isdigit():
                self.setSignificantFigures("Sistema Numerico Invalido")
                return
        
        self.calculateSignificantFigures()
    
   
    def calculateSignificantFigures(self):

        cleanNumber = self.number
        if cleanNumber.startswith('-') or cleanNumber.startswith('+'):
            cleanNumber = cleanNumber[1:]
        
        if cleanNumber == '0' or cleanNumber == '0.0':
            self.setSignificantFigures(0)
            return
        
        parts = cleanNumber.split('.')
        
        if len(parts) == 1:  
            numWithoutLeadingZeros = cleanNumber.lstrip('0')
            if not numWithoutLeadingZeros:  
                self.setSignificantFigures(0)
            else:
        
                lastNonZero =0
                for i in range(len(numWithoutLeadingZeros) - 1, -1, -1):
                    if numWithoutLeadingZeros[i] != '0':
                        lastNonZero = i + 1
                self.setSignificantFigures(lastNonZero)
        else:
            integerPart, decimalPart = parts
            
            
            if all(c == '0' for c in cleanNumber.replace('.', '')):
                
                self.setSignificantFigures(len(decimalPart) if decimalPart else 1)
                return
            
            
            if not integerPart or integerPart == '0' or all(c == '0' for c in integerPart):
                firstSignificant = 0
                found = False
                for i, digit in enumerate(decimalPart):
                    if not found and digit != '0':
                        firstSignificant = i
                        found = True
                
                significantDigits = decimalPart[firstSignificant:]
                self.setSignificantFigures(len(significantDigits))
            else:
                
                integerPartWithoutZeros = integerPart.lstrip('0')
                
                self.setSignificantFigures(len(integerPartWithoutZeros) + len(decimalPart))
    
    
    def calculateNormalizedForm(self):
        try:
            
            numFloat = float(self.number.replace(',', '.'))
            
            if self.getSignificantFigures() == "Sistema Numerico Invalido":
                self.normalizedForm = "Sistema Numerico Invalido"
                return
            if self.getSignificantFigures() == 0:
                self.normalizedForm = "0.0 x 10^0"
                return
            
            if numFloat == 0:
                self.normalizedForm = "0.0 x 10^0"
                return
            
            
            if abs(numFloat) >= 1:
                
                exponent = 0
                temp = abs(numFloat)
                while temp >= 10:
                    temp /= 10
                    exponent += 1
                mantissa = numFloat / (10 ** exponent)
            else:
               
                exponent = 0
                temp = abs(numFloat)
                while temp < 1:
                    temp *= 10
                    exponent -= 1
                mantissa = numFloat / (10 ** exponent)
            
            
            if exponent == 0:
                self.normalizedForm = f"{mantissa}"
            else:
                self.normalizedForm = f"{mantissa:.6g} x 10^{exponent}"
                
        except ValueError:
            self.normalizedForm = "Forma normalizada invalida"
    
   
    def toString(self):
        return f"Numero: {self.number} Cifras Significativas: {self.significantFigures} Forma Normalizada: {self.normalizedForm}"
    
    # Getters
    def getNumber(self):
        return self.number
    
    def getSignificantFigures(self):
        return self.significantFigures
    
    def getNormalizedForm(self):
        return self.normalizedForm
    
    # Setters
    def setNumber(self, number):
        self.number = str(number)
        self.checkDecimalSystem()
        self.calculateNormalizedForm()
    
    def setSignificantFigures(self, figures):
        self.significantFigures = figures
    
    def setNormalizedForm(self, normalizedForm):
        self.normalizedForm = normalizedForm