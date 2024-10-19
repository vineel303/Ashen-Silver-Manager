#importing libraries
import os
from natsort import natsorted
import time
import subprocess
import pygetwindow
import pyautogui
import shutil
from datetime import datetime
import pandas

#simple system constants
RESET = "\033[0m"
BRIGHT = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

#compound system constants
BRIGHT_RED = BRIGHT + RED
BRIGHT_YELLOW = BRIGHT + YELLOW
BRIGHT_GREEN = BRIGHT + GREEN
BRIGHT_BLUE = BRIGHT + BLUE
BRIGHT_MAGENTA = BRIGHT + MAGENTA
BRIGHT_CYAN = BRIGHT + CYAN

#large program constants
introStatement = f"""Artwork:
    {BRIGHT_RED}1. Camera's Position & Angle{RESET}
    A. Backdrops:
        {BRIGHT_RED}2. Objects
        3. Backdrops{RESET}
    B. Characters
        {BRIGHT_RED}4. Clothes
        5. Accessories
        6. Expressions
        7. Posture
        8. Face
            > Eyes
            > Hair
        9. Body
            > Bust-Waist-Hips{RESET}
Artist:
    {BRIGHT_RED}1. Colour
    2. Unique Art Style
    3. Novel Related Ideas{RESET}

Look:
    {BRIGHT_RED}1. Favourite
    2. Good{RESET}
Draw:
    {BRIGHT_RED}1. Recheck
    2. None{RESET}

{BRIGHT}--- --- ---{RESET}

1. {BRIGHT_YELLOW}Backdrop Elements{RESET}: Elements of a backdrop (like trees and clouds in a mountain backdrop).
2. {BRIGHT_YELLOW}Object vs Accessories{RESET}: Any object that a character is wearing/holding is an accessory, irrespective of size.
3. {BRIGHT_YELLOW}Eyes/Hair{RESET}: Colour & Unique Art Style
4. {BRIGHT_YELLOW}Posture wrt{RESET}: Character/s, Object/s, Backdrop/s, Camera.
5. {BRIGHT_YELLOW}Characters/Backdrops{RESET}: Upto few {DIM}(like day meeting night, or summer meeting winter){RESET}.
6. {BRIGHT_YELLOW}Accessories/Objects/Backdrop Elements{RESET}: Upto many. Small/big (in size). Unique or generic (in value).
"""

helpStatement = f"""{BRIGHT_RED}00{RESET} : Objects      | b
0{BRIGHT_RED}1{RESET} : Backdrops    | b
0{BRIGHT_RED}2{RESET} : Accessories  | +
0{BRIGHT_RED}3{RESET} : Clothes      | +
0{BRIGHT_RED}4{RESET} : Faces        | c
0{BRIGHT_RED}5{RESET} : Expressions  | c
0{BRIGHT_RED}6{RESET} : Postures     | c
0{BRIGHT_RED}7{RESET} : Colours      | g
0{BRIGHT_RED}8{RESET} : Uni-AS       | g
0{BRIGHT_RED}9{RESET} : NV           | g

Start with '{BRIGHT_RED}/ & Enter{RESET}' for R images.
{BRIGHT_RED}1{RESET}0 : 2 Objects    | b
{BRIGHT_RED}2{RESET}0 : 3 Objects    | b
Face #: {BRIGHT_RED}E{RESET}yes {BRIGHT_RED}H{RESET}air {BRIGHT_RED}C{RESET}olour {BRIGHT_RED}S{RESET}tyle.
DEL a b: delete

{BRIGHT_RED}30{RESET} : Grade A      | v
{BRIGHT_RED}31{RESET} : Grade B      | v
{BRIGHT_RED}32{RESET} : Recheck      | a
{BRIGHT_RED}33{RESET} : Non-AS       | a
{BRIGHT_RED}34{RESET} : Delete       | a
{BRIGHT_RED}35{RESET} : Body Shapes  | c
{BRIGHT_RED}36{RESET} : Camera P/A   | c
"""

folderAddressList = {

    #g0
    "00" : r"D:\Ashen Silver\1b Objects",
    "01" : r"D:\Ashen Silver\1b Backdrops",
    "02" : r"D:\Ashen Silver\1c Accessories",
    "03" : r"D:\Ashen Silver\1c Clothes",
    "04" : r"D:\Ashen Silver\1c Faces",
    "05" : r"D:\Ashen Silver\1c Expressions",
    "06" : r"D:\Ashen Silver\1c Postures",
    "07" : r"D:\Ashen Silver\1g Colours",
    "08" : r"D:\Ashen Silver\1g UniAS",
    "09" : r"D:\Ashen Silver\1g NV",

    #g1
    "10" : r"D:\Ashen Silver\2b Objects",
    "11" : r"D:\Ashen Silver\2b Backdrops",
    "12" : r"D:\Ashen Silver\2c Accessories",
    "13" : r"D:\Ashen Silver\2c Clothes",
    "14" : r"D:\Ashen Silver\2c Faces",
    "15" : r"D:\Ashen Silver\2c Expressions",
    "16" : r"D:\Ashen Silver\2c Postures",
    "17" : r"D:\Ashen Silver\2g Colours",
    "18" : r"D:\Ashen Silver\2g UniAS",
    "19" : r"D:\Ashen Silver\2g NV",

    #g2
    "20" : r"D:\Ashen Silver\3b Objects",
    "21" : r"D:\Ashen Silver\3b Backdrops",
    "22" : r"D:\Ashen Silver\3c Accessories",
    "23" : r"D:\Ashen Silver\3c Clothes",
    "24" : r"D:\Ashen Silver\3c Faces",
    "25" : r"D:\Ashen Silver\3c Expressions",
    "26" : r"D:\Ashen Silver\3c Postures",
    "27" : r"D:\Ashen Silver\3g Colours",
    "28" : r"D:\Ashen Silver\3g UniAS",
    "29" : r"D:\Ashen Silver\3g NV",

    #r0
    "00R" : r"D:\Ashen Silver\R\1b Objects",
    "01R" : r"D:\Ashen Silver\R\1b Backdrops",
    "02R" : r"D:\Ashen Silver\R\1c Accessories",
    "03R" : r"D:\Ashen Silver\R\1c Clothes",
    "04R" : r"D:\Ashen Silver\R\1c Faces",
    "05R" : r"D:\Ashen Silver\R\1c Expressions",
    "06R" : r"D:\Ashen Silver\R\1c Postures",
    "07R" : r"D:\Ashen Silver\R\1g Colours",
    "08R" : r"D:\Ashen Silver\R\1g UniAS",
    "09R" : r"D:\Ashen Silver\R\1g NV",

    #r1
    "10R" : r"D:\Ashen Silver\R\2b Objects",
    "11R" : r"D:\Ashen Silver\R\2b Backdrops",
    "12R" : r"D:\Ashen Silver\R\2c Accessories",
    "13R" : r"D:\Ashen Silver\R\2c Clothes",
    "14R" : r"D:\Ashen Silver\R\2c Faces",
    "15R" : r"D:\Ashen Silver\R\2c Expressions",
    "16R" : r"D:\Ashen Silver\R\2c Postures",
    "17R" : r"D:\Ashen Silver\R\2g Colours",
    "18R" : r"D:\Ashen Silver\R\2g UniAS",
    "19R" : r"D:\Ashen Silver\R\2g NV",

    #r2
    "20R" : r"D:\Ashen Silver\R\3b Objects",
    "21R" : r"D:\Ashen Silver\R\3b Backdrops",
    "22R" : r"D:\Ashen Silver\R\3c Accessories",
    "23R" : r"D:\Ashen Silver\R\3c Clothes",
    "24R" : r"D:\Ashen Silver\R\3c Faces",
    "25R" : r"D:\Ashen Silver\R\3c Expressions",
    "26R" : r"D:\Ashen Silver\R\3c Postures",
    "27R" : r"D:\Ashen Silver\R\3g Colours",
    "28R" : r"D:\Ashen Silver\R\3g UniAS",
    "29R" : r"D:\Ashen Silver\R\3g NV",

    #g3
    "30" : r"D:\Ashen Silver\More\Grade A",
    "31" : r"D:\Ashen Silver\More\Grade B",
    "32" : r"D:\Ashen Silver\More\ReCheck",
    "33" : r"D:\Ashen Silver\More\NonAS",
    "34" : r"D:\Ashen Silver\More\Delete",
    "35" : r"D:\Ashen Silver\5c Body Shapes",
    "36" : r"D:\Ashen Silver\5c Camera",
    "99" : r"D:\Ashen Silver\More\Great Library",

    #r3
    "30R" : r"D:\Ashen Silver\More\Grade A R",
    "31R" : r"D:\Ashen Silver\More\Grade B R",
    "32R" : r"D:\Ashen Silver\More\ReCheck R",
    "33R" : r"D:\Ashen Silver\More\NonAS R",
    "34R" : r"D:\Ashen Silver\More\Delete",
    "35R" : r"D:\Ashen Silver\R\5c Body Shapes",
    "36R" : r"D:\Ashen Silver\R\5c Camera",
    "99R" : r"D:\Ashen Silver\More\Great Library R",

}

#small program constants
path_masterFolder = r"D:\Ashen Silver\More\Master"
keysIn_folderAddressList = list(folderAddressList.keys())

#variables
filesInMasterFolder = []

#definitions
#defs
def p():
    print("")

def characterUpdater(character):
    inputCharacter  = ['/', '\\', '|', '?', '<', '>', '*', '"', ':']
    outputCharacter = ['Ⳇ', '⧵', '|', 'Ɂ', '˂', '˃', '⁎', "''", '։']
    if character in inputCharacter:
        return outputCharacter[inputCharacter.index(character)]
    return character

#defs
def updateAllFileNames():
    global path_masterFolder
    fileValue = 0
    for fileName in os.listdir(path_masterFolder):
        if os.path.isfile(os.path.join(path_masterFolder, fileName)):
            fileExtension = fileName.rsplit(".")
            fileExtension = fileExtension[-1]
            fileValue+=1
            newFileName = str(fileValue) + "." + fileExtension
            os.rename(os.path.join(path_masterFolder, fileName), os.path.join(path_masterFolder, newFileName))

def addFilesTo_filesInMasterFolder():
    global path_masterFolder
    global filesInMasterFolder
    for fileName in os.listdir(path_masterFolder):
        if os.path.isfile(os.path.join(path_masterFolder, fileName)):
            filesInMasterFolder.append(fileName)
    filesInMasterFolder = natsorted(filesInMasterFolder)

#defs
def allWindowSetup(imageWindow):
    global path_masterFolder
    windowSetup_windowSnap(r"C:\Users\vinee\AppData\Local\Programs\Python\Launcher\py.exe", "right")
    time.sleep(0.5)
    subprocess.run(['start', '', os.path.join(path_masterFolder, imageWindow)], shell=True)
    time.sleep(0.5)
    windowSetup_windowSnap(imageWindow, "left")
    windowSetup_windowSnapReposition()

def windowSetup_windowSnap(windowName, position):
    windowObject = pygetwindow.getWindowsWithTitle(windowName)
    if windowObject:
        windowObject = windowObject[0]
        windowObject.restore()
        windowObject.activate()
        windowObject.maximize()
        time.sleep(0.5)
        pyautogui.hotkey("win", position)
    else:
        time.sleep(0.25)
        windowSetup_windowSnap(windowName, position)

def windowSetup_windowSnapReposition():
    pyautogui.moveTo(960, 509)
    time.sleep(0.5)
    pyautogui.mouseDown()
    pyautogui.moveTo(1600, 509, duration=0.5)
    pyautogui.mouseUp()
    pyautogui.moveTo(1892, 69)
    windowObject = pygetwindow.getWindowsWithTitle(r"C:\Users\vinee\AppData\Local\Programs\Python\Launcher\py.exe")
    windowObject[0].activate()

def gotoNextImage(index):
    global filesInMasterFolder
    windowObject = pygetwindow.getWindowsWithTitle(filesInMasterFolder[index])
    windowObject[0].activate()
    pyautogui.press('right')
    windowObject = pygetwindow.getWindowsWithTitle(r"C:\Users\vinee\AppData\Local\Programs\Python\Launcher\py.exe")
    windowObject[0].activate()

def closeImageWindow(imageWindow):
    imageWindowObject = pygetwindow.getWindowsWithTitle(imageWindow)
    imageWindowObject[0].activate()
    pyautogui.hotkey("alt", "f4")

#defs
def readAndWriteTo_programSafety(value):
    fileObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Program Safety.txt", "rt")
    value_lastProgramSafety = int(fileObject.read())
    fileObject.close
    fileObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Program Safety.txt", "wt")
    fileObject.write(str(value))
    fileObject.close
    return value_lastProgramSafety

def readUniqueFileId():
    fileObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Unique File ID.txt", "rt")
    value_uniqueFileID = int(fileObject.read())
    fileObject.close()
    return value_uniqueFileID
    
def writeToUniqueFileId(value):
    fileObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Unique File ID.txt", "wt")
    fileObject.write(str(value))
    fileObject.close()

def uniqueFileID_repair(value):
    if value == 0:
        global value_uniqueFileID
        value_uniqueFileID+=100
        writeToUniqueFileId(value_uniqueFileID)




def database_repair():
    dbSize = os.path.getsize(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 1.csv")
    if dbSize > 100000:
        #os.remove(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 2.csv")
        #os.rename(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 1.csv", r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 2.csv")
        #shutil.copy(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Sample.csv", r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 1.csv")

        activeCsvPath = 
        inactiveCsvPath = 
        activeCsv = 
        sampleCsv = 
        shutil.move(os.path.join(activeCsvPath, activeCsv), os.path.join(inactiveCsvPath, activeCsv))
        shutil.copy(os.path.join(activeCsvPath, sampleCsv), os.path.join(activeCsvPath, activeCsv))
        
        if getFolderSize()>:





def getFolderSize(folderPath):
    folderSize = 0
    for varA, varB, fileNames in os.walk(folderPath):
        for fileName in fileNames:
            filePath = os.path.join(varA, fileName)
            folderSize += os.path.getsize(filePath)
    return folderSize

#defs
def copyRenamedFile(fileIndex):
    global value_uniqueFileID
    global path_masterFolder
    global filesInMasterFolder
    global keysIn_folderAddressList

    #base setup
    #1
    isR = False
    inputIndex = -1
    cmdList_keys = []
    cmdList_values = []

    #2
    osReservedFilenames = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    ]

    #3
    dateTimeNow = datetime.now()
    dateNow = dateTimeNow.strftime("%d-%m-%Y")
    timeNow = dateTimeNow.strftime("%H:%M:%S")

    #printing
    for i in range(10):
        p()
    print(helpStatement)

    print(filesInMasterFolder[fileIndex])
    p()

    #input
    while True:
        
        #getting input
        inputIndex+=1
        if inputIndex % 2 == 1:
            print(f"{MAGENTA}{inputIndex}: {RESET}{BRIGHT_GREEN}", end="")
            cmd = input()
            print(f"{RESET}")
        else:
            print(f"{MAGENTA}{inputIndex}: {RESET}{BRIGHT_BLUE}", end="")
            cmd = input()
            print(f"{RESET}")

        #checking input
        if cmd == "":
            break
        if cmd == "/":
            isR = True
            continue

        thisState = True
        if len(cmd)>3:
            if cmd[0:3].upper == "DEL":
                delete_cmd = cmd.split(" ")
                delete_cmd.pop(0)
                for dceIndex in range(len(delete_cmd)):
                    if delete_cmd[dceIndex] not in cmdList_keys:
                        print(f"'{delete_cmd[dceIndex]}' was not found. Retry.\n")
                        thisState = False
                        break
                if thisState:
                    for dceIndex in range(len(delete_cmd)):
                        thisValue = int(delete_cmd[dceIndex])
                        cmdList_values.pop(thisValue)
                        cmdList_keys.pop(thisValue)
                else:
                    continue                        
                        
        if len(cmd)<2:
            print(f"'{cmd}' is too short. Retry")
            p()
            continue
        elementKey = cmd[0:2]
        if elementKey not in keysIn_folderAddressList:
            print(f"'{elementKey}' is not a valid key. Retry.")
            p()
            continue
        elementValue = cmd[2:].strip()
        
        #updating invalid file names
        #part 1
        if elementValue.upper in osReservedFilenames:
            elementValue = elementValue + "_"
        #part 2
        stringAsList = list(elementValue)
        if stringAsList:
            stringAsList[0] = stringAsList[0].upper()
        for characterIndex in range(len(stringAsList)):
            stringAsList[characterIndex] = characterUpdater(stringAsList[characterIndex])
        elementValue = "".join(stringAsList)
        
        #accepting input
        cmdList_values.append(elementValue)
        if isR:
            cmdList_keys.append(elementKey + "R")
        else:
            cmdList_keys.append(elementKey)
    
    #goto next image
    gotoNextImage(fileIndex)
    
    #updating the lists
    addToTheGreatLibrary = True
    if isR:
        if "32R" in cmdList_keys:
            addToTheGreatLibrary=False
        if "34R" in cmdList_keys:
            addToTheGreatLibrary=False
        if addToTheGreatLibrary:
            cmdList_keys.append("99")
            cmdList_values.append("Nyan")
    else:
        if "32" in cmdList_keys:
            addToTheGreatLibrary=False
        if "34" in cmdList_keys:
            addToTheGreatLibrary=False
        if addToTheGreatLibrary:
            cmdList_keys.append("99R")
            cmdList_values.append("Nyan")
    
    for cmdListIndex in range(len(cmdList_keys)):
        value_uniqueFileID += 1
        writeToUniqueFileId(value_uniqueFileID)
        fileName = filesInMasterFolder[fileIndex]

        if len(cmdList_values[cmdListIndex]) > 200 :
            fileExtension = fileName.rsplit(".")[-1]
            newFileName = "Z as [" + cmdList_values[cmdListIndex][190] + "]..." + " - (" + value_uniqueFileID + ")." + fileExtension
            newFileName_forText = "Z as [" + cmdList_values[cmdListIndex][190] + "]..." + " - (" + value_uniqueFileID + ").txt"
            newFolderAddressKey = cmdList_keys[cmdListIndex]
            newAddress = keysIn_folderAddressList[newFolderAddressKey]
            #copying and renaming the files
            shutil.copy(os.path.join(path_masterFolder, fileName), os.path.join(newAddress, newFileName))
            #writing to the text file
            txtFileObject = open(os.path.join(newAddress, newFileName_forText), "wt", encoding="utf-8")
            txtFileObject.write(cmdList_values[cmdListIndex])
            txtFileObject.close()
            #sending data to csv
            dataToSend = {"Original Name":[fileName], "New Name":[newFileName], "Folder Key":[newFolderAddressKey], "Folder Address":[newAddress[16:]], "Has Z":["Yes"], "Date":[dateNow], "Time":[timeNow]}
            dataToSend_dataFrame = pandas.DataFrame(dataToSend)
            dataToSend_dataFrame.to_csv(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 1.csv", mode="a", encoding="utf-8", header=False, index=False)

        else:
            fileExtension = fileName.rsplit(".")[-1]
            newFileName = cmdList_values[cmdListIndex] + " - (" + str(value_uniqueFileID) + ")." + fileExtension
            newFolderAddressKey = cmdList_keys[cmdListIndex]
            newAddress = folderAddressList[newFolderAddressKey]
            #copying and renaming the files
            shutil.copy(os.path.join(path_masterFolder, fileName), os.path.join(newAddress, newFileName))
            #sending data to csv
            dataToSend = {"Original Name":[fileName], "New Name":[newFileName], "Folder Key":[newFolderAddressKey], "Folder Address":[newAddress[16:]], "Has Z":["No"], "Date":[dateNow], "Time":[timeNow]}
            dataToSend_dataFrame = pandas.DataFrame(dataToSend)
            dataToSend_dataFrame.to_csv(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History - 1.csv", mode="a", encoding="utf-8", header=False, index=False)

### ### ###

#main function
if __name__ == "__main__":
    #starting
    updateAllFileNames()
    time.sleep(0.1)
    addFilesTo_filesInMasterFolder()
    allWindowSetup(filesInMasterFolder[0])
    value_lastProgramSafety = readAndWriteTo_programSafety(0)
    value_uniqueFileID = readUniqueFileId()
    uniqueFileID_repair(value_lastProgramSafety)
    database_repair()
    print(introStatement)

    #main function of the main function
    for index in range(len(filesInMasterFolder)):
        copyRenamedFile(index)

    #ending
    readAndWriteTo_programSafety(1)
    closeImageWindow(filesInMasterFolder[-1])
    input("Finished. Press enter to exit.")

#the end
