class numericSystem:
    def __init__(self, number):
        self.number = str(number.strip())
        self.binSystem=None
        self.decSystem=None
        self.hexSystem=None
        self.numberBase10=None
        self.processNumericSystem()
        self.convertToBase10()

    def isBinary(self, s: str) -> bool:
        for c in s:
            if c not in "01":
                return False
        return True

    def isDecimal(self, s: str) -> bool:
        for c in s:
            if not ('0' <= c <= '9'):
                return False
        return True

    def isHexadecimal(self, s: str) -> bool:
        hexChars = "0123456789ABCDEFabcdef"
        for c in s:
            if c not in hexChars:
                return False
        return True

    def processNumericSystem(self):
        num = self.getNumber().replace(',', '.').strip()

        if num == '' or num == '%z'or num == '0':
            self.binSystem = False
            self.decSystem = False
            self.hexSystem = False
            return "Ninguna base válida"

        if num[0] in ['-', '+']:
            numNoSign = num[1:]
        else:
            numNoSign = num

        numNoDot = numNoSign.replace('.', '')

        if numNoDot == '':
            self.binSystem = False
            self.decSystem = False
            self.hexSystem = False
            return "Ninguna base válida"

        self.binSystem = self.isBinary(numNoDot)
        self.decSystem = self.isDecimal(numNoDot)
        self.hexSystem = self.isHexadecimal(numNoDot)

    def convertToBase10(self):
        num_str = self.number.replace(',', '.').strip()
        sign = 1
        if num_str.startswith('-'):
            sign = -1
            num_str = num_str[1:]
        elif num_str.startswith('+'):
            num_str = num_str[1:]
        
        if not num_str or num_str == '.':
            self.numberBase10 = None
            return
        
        parts = num_str.split('.', 1)
        integer_part = parts[0]
        fractional_part = parts[1] if len(parts) > 1 else ''
        
        if self.binSystem:
            base = 2
            integer_val = int(integer_part, base) if integer_part else 0
            fractional_val = 0
            for i, digit in enumerate(fractional_part):
                fractional_val += int(digit) * (base ** -(i + 1))
            self.numberBase10 = sign * float(num_str)
            
        elif self.decSystem:
            try:
                self.numberBase10 = sign * float(num_str)
            except ValueError:
                self.numberBase10 = None
                
        elif self.hexSystem:
            base = 16
            integer_val = int(integer_part, base) if integer_part else 0
            fractional_val = 0
            for i, digit in enumerate(fractional_part):
                digit_val = int(digit, base)
                fractional_val += digit_val * (base ** -(i + 1))
            self.numberBase10 = integer_val + fractional_val
        else:
            self.numberBase10 = 0

    #setters
    def setBinSystem(self,req:bool):
        self.binSystem=req

    def setDecSystem(self,req:bool):
        self.decSystem=req

    def setHexSystem(self,req:bool):
        self.hexSystem=req

    #getters

    def getBinSystem(self):
        return self.binSystem

    def getDecSystem(self):
        return self.decSystem

    def getHexSystem(self):
        return self.hexSystem

    def getNumber(self):
        return self.number
    def getNumberBase10(self):
        return (self.numberBase10)

    def toString(self):
        return f"El numero {self.number} pertenece a los sistemas numericos: {self.numberSystemInfo()}"

    def numberSystemInfo(self):
        result=""
        if self.binSystem==True:
            result+=" Binario "
        elif self.decSystem==True:
            result+=" Decimal"
        elif self.hexSystem==True:
            result +=" Hexadecimal"
        else:
            result="ERROR!"
        return result