
import os
import src.Helpers.DataGenerate as DataGenerate


def main():
    archiveGen = DataGenerate.archiveGenerator()
    archiveGen.setRouter(os.getcwd())
    for i in range(3):
        archiveGen.setName("randomFile"+str(i+1)+".bin")
        archiveGen.archiveDataGenerator()
    
main()