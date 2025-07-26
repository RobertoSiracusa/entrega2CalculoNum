import os
from datetime import datetime
import random

class ArchiveUtil:
    def __init__(self, router=""):
        if not router or not router.strip():
            raise ValueError("La ruta asignada no es válida.")
        self._router = None
        self.utilDirectory(router)
    
    @property
    def router(self):
        return self._router
    
    @router.setter
    def router(self, newRouter):
        self.utilDirectory(newRouter)
    
    def utilDirectory(self, router):
        if not os.path.exists(router):
            errorMsg = "El directorio a guardar no existe."

            if hasattr(self, '_router') and self._router:
                self.logError("FileNotFoundError", errorMsg)
            raise FileNotFoundError(errorMsg)
        self._router = router
    
    def getArchive(self, fileName):
        if not fileName or not fileName.strip():
            errorMsg = "El nombre del archivo es requerido."
            self.logError("ValueError", errorMsg)
            raise ValueError(errorMsg)
        
        fullFilePath = os.path.join(self._router, fileName)
        if not os.path.isfile(fullFilePath):
            errorMsg = "El archivo no se encontro en el directorio especificado."
            self.logError("FileNotFoundError", errorMsg)
            raise FileNotFoundError(errorMsg)
        
        return open(fullFilePath, 'rb')

    def setCreateArchiveLog(self, content, logFileName, outputLogFileName, appendNewline=False):

        fullFilePath = os.path.join(self._router, f"{logFileName}.log")
        mode = 'a' if os.path.exists(fullFilePath) else 'w'

        with open(fullFilePath, mode,encoding='utf-8') as file:
            file.write(outputLogFileName+content) 
            if appendNewline:
                file.write('\n')
                
    def setCreateArchiveTxt(self, content, fileName, appendNewline=False):

        if not content or not content.strip(): 
            raise ValueError("El contenido es requerido.")
        if not fileName:
            raise ValueError("El nombre del archivo es requerido.")

        fullFilePath = os.path.join(self._router, f"{fileName}.txt")
        mode = 'a' if os.path.exists(fullFilePath) else 'w'

        with open(fullFilePath, mode, encoding='utf-8') as file:
            file.write(content) 
            if appendNewline:
                file.write('\n')
    
    
    def getDirectories(self):
        if not os.path.exists(self._router):
            errorMsg = "El directorio no existe."
            self.logError("FileNotFoundError", errorMsg)
            raise FileNotFoundError(errorMsg)
        
        files = os.listdir(self._router)
        if not files:
            errorMsg = "No se encontraron archivos."
            self.logError("FileNotFoundError", errorMsg)
            raise FileNotFoundError(errorMsg)
        return files
    
    def directoriesExist(self):
        
        if not os.path.exists(self._router):
            return False  
        return bool(os.listdir(self._router))
    
    def logError(self, errorType, errorMessage):
        try:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            serial = random.randint(1, 99)

            logEntry = f"[{timestamp}-SERIAL_{serial}] ERROR - {errorType}\n"
            logEntry += f"  Mensaje: {errorMessage}\n"         
            self.setCreateArchiveLog(logEntry, " ", appendNewline=True, booleano=False)
            
        except Exception as logException:

            print(f"Warning: No se pudo registrar el error en el log: {logException}")