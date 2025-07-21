
import os
import src.Helpers.DataGenerate as DataGenerate

storage="src\Storage"
def main():
    archiveGen = DataGenerate.archiveGenerator()
    archiveGen.setRouter(os.getcwd()+"src/Storage")
    for i in range(3):
        archiveGen.setName("randomFile"+str(i+1)+".bin")
        archiveGen.archiveDataGenerator()
    
main()