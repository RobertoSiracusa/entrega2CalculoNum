import os
import random

class archiveGenerator():
    __router = ""
    __nameArchive = ""

    def __init__(self, nameArchive = "generalArchive.bin", router = os.getcwd()):
        
        if (not router or len(router) == 0):
            raise Exception("Manage-Error: La ruta es vacia.")
        
        if (len(nameArchive) == 0 or not nameArchive):
            raise Exception("Manage-Error: La ruta es vacia.")
        
        self.__nameArchive = nameArchive
        self.__utilDirectory(router)

    def setRouter(self, router):
        
        if (not router or len(router) == 0):
            raise Exception("Manage-Error: La ruta es vacia.")
        self.utilDirectory(router)

    def setName(self, nameArchive):
        
        if (not nameArchive or len(nameArchive) == 0):
            raise Exception("Manage-Error: La ruta es vacia.")
        
        self.__nameArchive= nameArchive 

    def __setOrCreateFiles(self, nameArchive, content = "", bool = False):
        
        if (not nameArchive or len(nameArchive) == 0):
            raise Exception("Manage-Error: El nombre esta Vacio.")
        
        try: 
            if (not content or len(content) == 0):
                archive = open(self.__router+"\\"+nameArchive+".txt", "x")
                return
            
            archive = open(self.__router+"\\"+nameArchive, "a")
            
            if (bool == True):
                archive.write(content+"\n")
            else:
                archive.write(content)

        except FileNotFoundError as e:
            print("Manage-Error: El archivo no ha sido encontrado", e)

    def archiveDataGenerator(self, row = 3, colum = 3):
        
        arrayBi = []

        if(row > 0 and colum > 0):
            arrayBi = [[random.randint(-30, 30) for j in range(colum)] for i in range(row)]

            for i in range(len(arrayBi)):
                for j in range(len(arrayBi[0])):
                    if(j == (len(arrayBi[0]) - 1)):
                        self.__setOrCreateFiles(self.__nameArchive, str(arrayBi[i][j]), i < (len(arrayBi) - 1))
                    else:
                        self.__setOrCreateFiles(self.__nameArchive, str(arrayBi[i][j])+"#")

    def __utilDirectory(self, router):
        
        if (os.path.exists(router) and not os.path.isdir(router)):
            raise NotADirectoryError(f"Manage-Error: La ruta '{router}' no es un directorio.")
        elif (not os.path.exists(router)):
            raise FileNotFoundError(f"Manage-Error: El directorio '{router}' no existe.")
        
        self.__router = router


if __name__ == "__main__":
    output_directory = "src\\Storage\\"

    for i in range(1, 4):
        file_name = f"randomFile{i}.bin"
        
        try:
            
            generator = archiveGenerator(nameArchive=file_name, router=output_directory)
            
            generator.archiveDataGenerator(row=3, colum=3)
            print(f"Archivo '{file_name}' generado exitosamente en '{output_directory}'")
        except Exception as e:
            print(f"Error al generar el archivo '{file_name}': {e}")