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
            error_msg = "El directorio a guardar no existe."
            # Solo hacer log si _router ya está inicializado (evitar recursión en constructor)
            if hasattr(self, '_router') and self._router:
                self.logError("FileNotFoundError", error_msg)
            raise FileNotFoundError(error_msg)
        self._router = router
    
    def getArchive(self, fileName):
        if not fileName or not fileName.strip():
            error_msg = "El nombre del archivo es requerido."
            self.logError("ValueError", error_msg)
            raise ValueError(error_msg)
        
        fullFilePath = os.path.join(self._router, fileName)
        if not os.path.isfile(fullFilePath):
            error_msg = "El archivo no se encontro en el directorio especificado."
            self.logError("FileNotFoundError", error_msg)
            raise FileNotFoundError(error_msg)
        
        return open(fullFilePath, 'rb')

    def setCreateArchiveLog(self, content, logFileName, outputLogFileName, append_newline=False):

        fullFilePath = os.path.join(self._router, f"{logFileName}.log")
        mode = 'a' if os.path.exists(fullFilePath) else 'w'

        with open(fullFilePath, mode) as file:
            file.write(outputLogFileName+content) 
            if append_newline:
                file.write('\n')
    def setCreateArchiveTxt(self, content, fileName, append_newline=False):

        if not content or not content.strip(): 
            raise ValueError("El contenido es requerido.")
        if not fileName:
            raise ValueError("El nombre del archivo es requerido.")

        fullFilePath = os.path.join(self._router, f"{fileName}.txt")
        mode = 'a' if os.path.exists(fullFilePath) else 'w'

        with open(fullFilePath, mode) as file:
            file.write(content) 
            if append_newline:
                file.write('\n')
    
    
    def getDirectories(self):
        if not os.path.exists(self._router):
            error_msg = "El directorio no existe."
            self.logError("FileNotFoundError", error_msg)
            raise FileNotFoundError(error_msg)
        
        files = os.listdir(self._router)
        if not files:
            error_msg = "No se encontraron archivos."
            self.logError("FileNotFoundError", error_msg)
            raise FileNotFoundError(error_msg)
        return files
    
    def directoriesExist(self):
        
        if not os.path.exists(self._router):
            return False  
        return bool(os.listdir(self._router))
    
    def logError(self, error_type, error_message):
        try:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            serial = random.randint(1, 99)

            log_entry = f"[{timestamp}-SERIAL_{serial}] ERROR - {error_type}\n"
            log_entry += f"  Mensaje: {error_message}\n"         
            self.setCreateArchive(log_entry, " ", append_newline=True, booleano=False)
            
        except Exception as log_exception:
            # Si falla el logging, no queremos que rompa la funcionalidad principal
            print(f"Warning: No se pudo registrar el error en el log: {log_exception}")