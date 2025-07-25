from Helpers.utils import logWriter


class elementalOperation:
    def __init__(self, numberString, binSystem=None, decSystem=None, hexSystem=None):
        self.numberString = numberString
        self.elementalOperation = ""
        self.binSystem = binSystem
        self.decSystem = decSystem
        self.hexSystem = hexSystem
        self.elementalOperationResult = ""
        self._determineAvailableOperations()

    def _determineAvailableOperations(self):
        if self.decSystem==True:
            self._detDecOperation()
        if self.binSystem==True:
            self._detBinOperation()
        if self.hexSystem==True:
            self._detHexOperation()
        if not self.decSystem and not self.binSystem and not self.hexSystem:
            logWriter("ERROR:El numero no es un numero valido en ningun sistema.", True)
            self.elementalOperationResult = "No hay operaciones disponibles para el numero proporcionado."
    def _detHexOperation(self):
        hexNumber= self.numberString.replace(',', '.').strip()
        if not self.hexSystem:
            logWriter("ERROR:El numero no es un numero hexadecimal valido.", True)
            return
        if hexNumber == '0' or hexNumber == '0.0':
            logWriter("ERROR:No hay operaciones disponibles para el numero 0.",True)
            return
        output = f"Operaciones disponibles para el numero en base hexadecimal {hexNumber}:\n"   
        sum= self.hexSum()
        sub= self.hexSubtraction()
        mult= self.hexMultiplication()
        div= self.hexDivision()
        if sum==True:
            output=output + "Suma"
        if sub==True:
            output+= "Resta."
        if mult==True:
            output += "Multiplicacion,"
        if div==True:
            output += "Division."
        output += "\t"
        self.elementalOperationResult = f"Operaciones disponibles para el numero en base hexadecimal {hexNumber}:Suma, Resta, Multiplicacion, Division"
   
    def hexSum(self):
        hexNumber= self.numberString.replace(',', '.').strip()
        
        try:
            hexNumber=float(int(hexNumber, 16))
            result = 0
            
            i=0
            for i in range(int(hexNumber)):
                result = result+ 1
            return True
        except Exception as e:
            return False
    
    def hexSubtraction(self):
        hexNumber= self.numberString.replace(',', '.').strip()
        
        try:
            hexNumber=float(int(hexNumber, 16))
            result = 0
            for i in range(0,int(hexNumber)):
                result = result- 1
            return True
        except Exception as e:
            return False
    def hexMultiplication(self):
        hexNumber= self.numberString.replace(',', '.').strip()
        
        try:
            hexNumber=float(int(hexNumber, 16))
            result = 1
            for i in range(0,int(hexNumber)):
                result = result* 1
            return True
        except Exception as e:
            return False
    def hexDivision(self):
        hexNumber= self.numberString.replace(',', '.').strip()
        
        try:
            hexNumber=float(int(hexNumber, 16))
            result = 1
            for i in range(0,int(hexNumber)):
                result = result/ 1
            return True
        except Exception as e:
            return False
    def _detBinOperation(self):
        binNumber= self.numberString.replace(',', '.').strip()
        # Validar si el numero es binario
        if not all(char in '01.' for char in binNumber):
            self.binSystem = False
            logWriter("ERROR:El numero no es un numero binario valido.", True)
            
        elif not self.binSystem:
            logWriter("ERROR:El numero no es un numero binario valido.", True)
            
        elif binNumber == '0' or binNumber == '0.0':
            logWriter("ERROR:No hay operaciones disponibles para el numero 0.",True)
            
        else:
            parts = binNumber.split('.', 1)
            integerPart = parts[0]
            self.numberString = integerPart
            output = f"Operaciones disponibles para el numero en base binaria {binNumber}:\n"
            sum= self.binSum()
            sub= self.binSubtraction()
            mult= self.binMultiplication()
            div= self.binDivision()
            if sum==True:
                output=output + "Suma"
            if sub==True:
                output+= "Resta."
            if mult==True:
                output += "Multiplicacion,"
            if div==True:
                output += "Division."
            output += "\t"
            self.elementalOperationResult = output
    def binSum(self):
        binNumber= self.numberString.replace(',', '.').strip()
        
        try:
            binNumber = int(binNumber, 2)
            result = 0
            
            i=0
            for i in range(int(binNumber)):
                result = result+ 1
            return True
        except Exception as e:
            logWriter(f"Error en la suma binaria: {e}", True)
            return False
    def binSubtraction(self):
        binNumber= self.numberString.replace(',', '.').strip()
        try:
            binNumber = int(binNumber, 2)
            result = 0
            for i in range(0,int(binNumber)):
                result = result- 1
            return True
        except Exception as e:
            logWriter(f"Error en la resta binaria: {e}", True)
            return False
    def binMultiplication(self):
        binNumber= self.numberString.replace(',', '.').strip()
        
        try:
            binNumber = int(binNumber, 2)
            result = 1
            for i in range(0,int(binNumber)):
                result = result* 1
            return True
        except Exception as e:
            logWriter(f"Error en la multiplicacion binaria: {e}", True)
            return False
    def binDivision(self):
        binNumber= self.numberString.replace(',', '.').strip()
        
        try:
            binNumber = int(binNumber, 2)
            result = 1
            for i in range(0,int(binNumber)):
                result = result/ 1
            return True
        except Exception as e:
            logWriter(f"Error en la division binaria: {e}", True)
            return False
    

    def _detDecOperation(self):
        decNumber= self.numberString.replace(',', '.').strip()
        if not self.decSystem:
            logWriter("ERROR:El numero no es un numero decimal valido.", True)
            return
        if decNumber == '0' or decNumber == '0.0':
            logWriter("ERROR:No hay operaciones disponibles para el numero 0.",True)
            return
        output = f"Operaciones disponibles para el numero en base decimal {decNumber}:\n"
        sum= self.decSum()
        sub= self.decSubtraction()
        mult= self.decMultiplication()
        div= self.decDivision()
        
        if sum==True:
            output=output + "Suma"
        if sub==True:
            output+= "Resta."
        if mult==True:
            output += "Multiplicacion,"
        if div==True:
            output += "Division."
        output += "\t"

        self.elementalOperationResult = f"Operaciones disponibles para el numero en base decimal {decNumber}:Suma, Resta, Multiplicacion, Division"
        

    def decSum(self):
        decNumber= self.numberString.replace(',', '.').strip()
        
        try:
            decNumber=float(decNumber)
            result = 0
            
            i=0
            for i in range(int(decNumber)):
                result = result+ 1
            return "1"
        except Exception as e:
            logWriter(f"Error en la suma decimal: {e}", True)
            return False
    def decSubtraction(self):
        decNumber= self.numberString.replace(',', '.').strip()
        
        try:
            decNumber=float(decNumber)
            result = 0
            for i in range(0,int(decNumber)):
                result = result- 1
            return True
        except Exception as e:
            logWriter(f"Error en la resta decimal: {e}", True)
            return False
    def decMultiplication(self):
        decNumber= self.numberString.replace(',', '.').strip()
        
        try:
            decNumber=float(decNumber)
            result = 1
            for i in range(0,int(decNumber)):
                result = result* 1
            return True
        except Exception as e:
            logWriter(f"Error en la multiplicacion decimal: {e}", True)
            return False
    def decDivision(self):
        decNumber = self.numberString.replace(',', '.').strip()
        
        try:
            decNumber = float(decNumber)
            result = 1

            for i in range(int(decNumber)):
                result = result / 1
            return True
        except Exception as e:
            logWriter(f"Error en la division decimal: {e}", True)
            return False

       
        
    def toString(self):
        if self.elementalOperationResult == "":
            return "No hay operaciones disponibles para el numero proporcionado."
        return self.elementalOperationResult

