import Repositories.archiveUtil as ArchiveUtil 
import random
import datetime

def logWriter(content,append_newLine):
    pathToFile = "src/Storage"
    archive = ArchiveUtil.ArchiveUtil(pathToFile)

    currentDateTime = datetime.datetime.now()
    formattedDateTime = currentDateTime.strftime("%Y-%m-%d_%H-%M-%S")
    randNum = random.randint(1, 99)
    outputLogFileName = f"ErrorLog[{formattedDateTime}_serial{randNum}]:"
    logFileName="ErrorReport"

    archive.setCreateArchiveLog(content,logFileName,outputLogFileName,append_newLine)

def txtWriter(outputFileName, content, append_newLine=True):
    pathToFile = "src/Storage"
    archive = ArchiveUtil.ArchiveUtil(pathToFile)


    archive.setCreateArchiveTxt(content, outputFileName, append_newLine)