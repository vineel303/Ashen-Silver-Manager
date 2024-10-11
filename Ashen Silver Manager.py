#importing libraries
import os
from natsort import natsorted
import time
import subprocess
import pygetwindow
import pyautogui
import shutil
import pandas
from datetime import datetime

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

#program variables
filesInMasterFolder = []

#small program constants
path_masterFolder = r"D:\Ashen Silver\More\Master"

#large program constants
#lpc
fullHelp_statement = f"""Elements:
    {BRIGHT_YELLOW}1. The camera's position{RESET}
    Non-living:
        {BRIGHT_YELLOW}2A. Scenery{RESET}{DIM} - Includes generic elements (like several normal trees, a normal river), and unique elements (like several white-leafed trees, a glowing river).{RESET}
        {BRIGHT_YELLOW}2B. Objects{RESET}{DIM} - Includes generic elements (like books, a phone), and unique elements (like black-paged books, a transparent phone).{RESET}
    Living:
        {BRIGHT_YELLOW}3A. Clothes{RESET}
        {BRIGHT_YELLOW}3B. Accessories{RESET} {DIM}- Includes small elements (like hair scrunchies), and big elements (like a school bag, a football in one's arms).{RESET}
        Face:
            {BRIGHT_YELLOW}3C1. Expression{RESET}
            {BRIGHT_YELLOW}3C2. Face{RESET}:
                {BRIGHT_YELLOW}> Eyes{RESET}{DIM} - Colour/Shape{RESET}
                {BRIGHT_YELLOW}> Hair{RESET}{DIM} - Colour/Shape{RESET}
        Body:
            {BRIGHT_YELLOW}3D1. Posture{RESET}{DIM} - wrt: another human/s, an object/s, the scenery, the camera.{RESET}
            {BRIGHT_YELLOW}3D2. Body{RESET}:
                {BRIGHT_YELLOW}> Bust-waist-hips{RESET}
Artist:
    {BRIGHT_YELLOW}Colours{RESET}
    {BRIGHT_YELLOW}Unique Art Style{RESET}
    {BRIGHT_YELLOW}Novel related ideas{RESET}
--- --- ---
Anime:
    {BRIGHT_YELLOW}Favourites{RESET}
    {BRIGHT_YELLOW}Good{RESET}
    {BRIGHT_YELLOW}The great library{RESET}
Ashen Silver:
    {BRIGHT_YELLOW}Delete{RESET}
    {BRIGHT_YELLOW}None{RESET}
    {BRIGHT_YELLOW}Rescan{RESET}

{DIM}(Scroll up for help.){RESET}
"""

#lpc
help_statement = f"""{BRIGHT_BLUE}00{RESET} : Objects          (b)
0{BRIGHT_BLUE}1{RESET} : Scenery          (b)
0{BRIGHT_BLUE}2{RESET} : Accessories      (+)
0{BRIGHT_BLUE}3{RESET} : Clothing         (+)
0{BRIGHT_BLUE}4{RESET} : Faces            (c)
0{BRIGHT_BLUE}5{RESET} : Expressions      (c)
0{BRIGHT_BLUE}6{RESET} : Posture          (c)
0{BRIGHT_BLUE}7{RESET} : Colours          (g)
0{BRIGHT_BLUE}8{RESET} : Uni-AS           (g)
0{BRIGHT_BLUE}9{RESET} : NV               (g)

Start with '{BRIGHT_BLUE}/{RESET}' for R images
{BRIGHT_BLUE}1{RESET}0 : 2 Objects        (b)
{BRIGHT_BLUE}2{RESET}0 : 3 Objects        (b)
Face: # {BRIGHT_BLUE}E{RESET}yes {BRIGHT_BLUE}H{RESET}air {BRIGHT_BLUE}C{RESET}olour {BRIGHT_BLUE}S{RESET}hape

{BRIGHT_BLUE}30{RESET} : Grade A          (V)
{BRIGHT_BLUE}31{RESET} : Grade B          (V)
{BRIGHT_BLUE}32{RESET} : Recheck          (a)
{BRIGHT_BLUE}33{RESET} : Non-AS           (a)
{BRIGHT_BLUE}34{RESET} : Delete           (a)
{BRIGHT_BLUE}35{RESET} : Body shape       (c)
{BRIGHT_BLUE}36{RESET} : Camera position  (c)
"""

#lpc
folderAddressList = {
    #G0
    '00' : r"D:\Ashen Silver\1 b Objects",
    '01' : r"D:\Ashen Silver\1 b Scenery",
    '02' : r"D:\Ashen Silver\1 c Accessories",
    '03' : r"D:\Ashen Silver\1 c Clothing",
    '04' : r"D:\Ashen Silver\1 c Faces",
    '05' : r"D:\Ashen Silver\1 c Expressions",
    '06' : r"D:\Ashen Silver\1 c Posture",
    '07' : r"D:\Ashen Silver\1 g Colours",
    '08' : r"D:\Ashen Silver\1 g UniAS",
    '09' : r"D:\Ashen Silver\1 g NV",
    #G1
    '10' : r"D:\Ashen Silver\2 b Objects",
    '11' : r"D:\Ashen Silver\2 b Scenery",
    '12' : r"D:\Ashen Silver\2 c Accessories",
    '13' : r"D:\Ashen Silver\2 c Clothing",
    '14' : r"D:\Ashen Silver\2 c Faces",
    '15' : r"D:\Ashen Silver\2 c Expressions",
    '16' : r"D:\Ashen Silver\2 c Posture",
    '17' : r"D:\Ashen Silver\2 g Colours",
    '18' : r"D:\Ashen Silver\2 g UniAS",
    '19' : r"D:\Ashen Silver\2 g NV",
    #G2
    '20' : r"D:\Ashen Silver\3 b Objects",
    '21' : r"D:\Ashen Silver\3 b Scenery",
    '22' : r"D:\Ashen Silver\3 c Accessories",
    '23' : r"D:\Ashen Silver\3 c Clothing",
    '24' : r"D:\Ashen Silver\3 c Faces",
    '25' : r"D:\Ashen Silver\3 c Expressions",
    '26' : r"D:\Ashen Silver\3 c Posture",
    '27' : r"D:\Ashen Silver\3 g Colours",
    '28' : r"D:\Ashen Silver\3 g UniAS",
    '29' : r"D:\Ashen Silver\3 g NV",
    #R0
    '00R' : r"D:\Ashen Silver\R9\1 b Objects",
    '01R' : r"D:\Ashen Silver\R9\1 b Scenery",
    '02R' : r"D:\Ashen Silver\R9\1 c Accessories",
    '03R' : r"D:\Ashen Silver\R9\1 c Clothing",
    '04R' : r"D:\Ashen Silver\R9\1 c Faces",
    '05R' : r"D:\Ashen Silver\R9\1 c Expressions",
    '06R' : r"D:\Ashen Silver\R9\1 c Posture",
    '07R' : r"D:\Ashen Silver\R9\1 g Colours",
    '08R' : r"D:\Ashen Silver\R9\1 g UniAS",
    '09R' : r"D:\Ashen Silver\R9\1 g NV",
    #R1
    '10R' : r"D:\Ashen Silver\R9\2 b Objects",
    '11R' : r"D:\Ashen Silver\R9\2 b Scenery",
    '12R' : r"D:\Ashen Silver\R9\2 c Accessories",
    '13R' : r"D:\Ashen Silver\R9\2 c Clothing",
    '14R' : r"D:\Ashen Silver\R9\2 c Faces",
    '15R' : r"D:\Ashen Silver\R9\2 c Expressions",
    '16R' : r"D:\Ashen Silver\R9\2 c Posture",
    '17R' : r"D:\Ashen Silver\R9\2 g Colours",
    '18R' : r"D:\Ashen Silver\R9\2 g UniAS",
    '19R' : r"D:\Ashen Silver\R9\2 g NV",
    #R2
    '20R' : r"D:\Ashen Silver\R9\3 b Objects",
    '21R' : r"D:\Ashen Silver\R9\3 b Scenery",
    '22R' : r"D:\Ashen Silver\R9\3 c Accessories",
    '23R' : r"D:\Ashen Silver\R9\3 c Clothing",
    '24R' : r"D:\Ashen Silver\R9\3 c Faces",
    '25R' : r"D:\Ashen Silver\R9\3 c Expressions",
    '26R' : r"D:\Ashen Silver\R9\3 c Posture",
    '27R' : r"D:\Ashen Silver\R9\3 g Colours",
    '28R' : r"D:\Ashen Silver\R9\3 g UniAS",
    '29R' : r"D:\Ashen Silver\R9\3 g NV",
    #G3
    '30' : r"D:\Ashen Silver\More\Grade A",
    '31' : r"D:\Ashen Silver\More\Grade B",
    '32' : r"D:\Ashen Silver\More\ReCheck",
    '33' : r"D:\Ashen Silver\More\NonAS",
    '34' : r"D:\Ashen Silver\More\Del",
    '35' : r"D:\Ashen Silver\5 c Body Shape",
    '36' : r"D:\Ashen Silver\5 c Camera Position",
    '99' : r"D:\Ashen Silver\More\The Great Library",
    #R3
    '30R' : r"D:\Ashen Silver\More\Grade A R9",
    '31R' : r"D:\Ashen Silver\More\Grade B R9",
    '32R' : r"D:\Ashen Silver\More\ReCheck R9",
    '33R' : r"D:\Ashen Silver\More\NonAS R9",
    '34R' : r"D:\Ashen Silver\More\Del",
    '35R' : r"D:\Ashen Silver\R9\5 c Body Shape",
    '36R' : r"D:\Ashen Silver\R9\5 c Camera Position",
    '99R' : r"D:\Ashen Silver\More\The Great Library R9",
}

keysIn_folderAddressList = list(folderAddressList.keys())

#functions
#funcs
def p():
    print("")

def getDbSize():
    dbSize = os.path.getsize(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History.csv")
    if dbSize>50000000:
        print(f"{BRIGHT_RED}Size of 'User's Command History.csv' is over 50 MB.{RESET}")
        p()

def addFilesTo_filesInMasterFolder():
    global path_masterFolder
    global filesInMasterFolder
    for fileName in os.listdir(path_masterFolder):
        if os.path.isfile(os.path.join(path_masterFolder, fileName)):
            filesInMasterFolder.append(fileName)
    filesInMasterFolder = natsorted(filesInMasterFolder)

#funcs
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
    pyautogui.click()

def gotoNextImage():
    pyautogui.moveTo(1287, 510)
    pyautogui.click()
    pyautogui.moveTo(1892, 69)
    pyautogui.click()

#funcs
def readAndWriteTo_programSafety(value):
    programSafetyObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Program Safety.txt", "rt")
    programSafety_lastValue = int(programSafetyObject.read())
    programSafetyObject.close
    programSafetyObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Program Safety.txt", "wt")
    programSafetyObject.write(str(value))
    programSafetyObject.close
    return programSafety_lastValue

def readUniqueFileId():
    uniqueFileIdObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Unique File ID.txt", "rt")
    uniqueFileId_lastValue = int(uniqueFileIdObject.read())
    uniqueFileIdObject.close
    return uniqueFileId_lastValue

def writeToUniqueFileId(value):
    uniqueFileIdObject = open(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\Unique File ID.txt", "wt")
    uniqueFileIdObject.write(str(value))
    uniqueFileIdObject.close

def updateUniqueFileId_ifBad(lastValue):
    if lastValue==0:
        global uniqueFileId_value
        print(f"{BRIGHT_RED}Last program safety was found Off.{RESET}")
        p()
        uniqueFileId_value += 100
        writeToUniqueFileId(uniqueFileId_value)

#funcs
def characterUpdater(character):
    inputCharacter = ['\\', '|', '?', '<', '>', '*', '"' , ':']
    outputCharacter = ['∖', '|', 'Ɂ', '˂', '˃', '⁎', "''", '։']
    if character in inputCharacter:
        return outputCharacter[inputCharacter.index(character)]
    return character

def renameFile_getCommand(fileName):
    global path_masterFolder
    global uniqueFileId_value
    dateTimeNow = datetime.now()
    dateNow = dateTimeNow.strftime("%d-%m-%Y")
    timeNow = dateTimeNow.strftime("%H:%M:%S")
    #printing
    for i in range(12):
        p()
    print(help_statement)
    #getting input
    print(f"{MAGENTA}Enter: {RESET}{BRIGHT_GREEN}", end="")
    cmd = input()
    print(f"{RESET}\n")
    if cmd[0]=="/":
        isR = True
    else:
        isR = False
    cmdList = cmd.split("/")
    if isR:
        cmdList.pop(0)
    cmdList_keys = []
    cmdList_values = []
    #checking validity
    for i in range(len(cmdList)):
        if len(cmdList[i])<2:
            print(f"{RED}'{cmdList[i]}' is too short. Retry.{RESET}")
            renameFile_getCommand(fileName)
        if cmdList[i][0:2] not in keysIn_folderAddressList:
            print(f"{RED}'{cmdList[i][0:2]}' in '{cmdList[i]}' is an invalid key. Retry.{RESET}")
            renameFile_getCommand(fileName)
    #going to the next image
    gotoNextImage()
    #creating lists
    for i in range(len(cmdList)):
        cmdList_keysElement = cmdList[i][0:2]
        cmdList_valuesElement = cmdList[i][2:]
        if isR:
            cmdList_keysElement = cmdList_keysElement + "R"
        cmdList_valuesElement = cmdList_valuesElement.strip()
        cmdList_keys.append(cmdList_keysElement)
        cmdList_values.append(cmdList_valuesElement)
    #updating lists
    tVar3 = True
    if isR:
        if ("32R" in cmdList_keys):
            tVar3 = False
        if ("34R" in cmdList_keys):
            tVar3 = False
        if tVar3:
            cmdList_keys.append("99R")
            cmdList_values.append("Nyan")
    else:
        if ("32" in cmdList_keys):
            tVar3 = False
        if ("34" in cmdList_keys):
            tVar3 = False
        if tVar3:
            cmdList_keys.append("99")
            cmdList_values.append("Nyan")
    #updating invalid file names
    osReservedFilenames = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    ]
    for tVar1 in range(len(cmdList_keys)):
        #part 1
        if cmdList_values[tVar1].upper() in osReservedFilenames:
            cmdList_values[tVar1] = cmdList_values[tVar1] + "_"
        #part 2
        stringObject_list = list(cmdList_values[tVar1])
        for tVar2 in range(len(stringObject_list)):
            stringObject_list[tVar2] = characterUpdater(stringObject_list[tVar2])
        cmdList_values[tVar1] = "".join(stringObject_list)
    #copying and renaming files
    for activeIndex in range(len(cmdList_keys)):
        uniqueFileId_value+=1
        writeToUniqueFileId(uniqueFileId_value)
        if len(cmdList_values[activeIndex]) <= 190:
            fileExtension = fileName.rsplit(".")
            fileExtension = fileExtension[1]
            newFileName = cmdList_values[activeIndex] + " - (" + str(uniqueFileId_value) + ")." + fileExtension
            newFolderAddressKey = cmdList_keys[activeIndex]
            #copying and renaming the file
            shutil.copy(os.path.join(path_masterFolder, fileName), os.path.join(folderAddressList[newFolderAddressKey], newFileName))
            #sending the user command to the csv database
            dataToSend = {"Original Name":[fileName], "New Name":[newFileName], "Folder Key":[newFolderAddressKey], "Folder Address":[folderAddressList[newFolderAddressKey][15:]], "Has Z":["No"], "Date":[dateNow], "Time":[timeNow]}
            dataToSend_dataFrom = pandas.DataFrame(dataToSend)
            dataToSend_dataFrom.to_csv(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History.csv", mode="a", header=False, index=False)
        else:
            fileExtension = fileName.rsplit(".")
            fileExtension = fileExtension[1]
            newFileName = "Z as [" + cmdList_values[activeIndex][0:180] + "]... - (" + str(uniqueFileId_value) + ")." + fileExtension
            newFileName_forTextFile = "Z as [" + cmdList_values[activeIndex][0:180] + "]... - (" + str(uniqueFileId_value) + ").txt"
            newFolderAddressKey = cmdList_keys[activeIndex]
            #copying and renaming the file
            shutil.copy(os.path.join(path_masterFolder, fileName), os.path.join(folderAddressList[newFolderAddressKey], newFileName))
            #creating the new text file
            txtFileObject = open(os.path.join(folderAddressList[newFolderAddressKey], newFileName_forTextFile), "wt", encoding="utf-8")
            txtFileObject.write(cmdList_values[activeIndex])
            txtFileObject.close()
            #sending the user command to the csv database
            dataToSend = {"Original Name":[fileName], "New Name":[newFileName], "Folder Key":[newFolderAddressKey], "Folder Address":[folderAddressList[newFolderAddressKey][15:]], "Has Z":["Yes"], "Date":[dateNow], "Time":[timeNow]}
            dataToSend_dataFrom = pandas.DataFrame(dataToSend)
            dataToSend_dataFrom.to_csv(r"E:\Code\Laptop Code\Ashen Silver Manager\Database\User's Command History.csv", mode="a", header=False, index=False)

#main function
if __name__ == "__main__":
    #starting
    addFilesTo_filesInMasterFolder()
    allWindowSetup(filesInMasterFolder[0])
    lastProgramSafety_value = readAndWriteTo_programSafety(0)
    uniqueFileId_value = readUniqueFileId()
    print(fullHelp_statement)
    updateUniqueFileId_ifBad(lastProgramSafety_value)
    getDbSize()
    
    #main function of the main function
    for fileName in filesInMasterFolder:
        renameFile_getCommand(fileName)
    
    #ending
    readAndWriteTo_programSafety(1)
    input("Finished. Press enter to exit.")
    pyautogui.moveTo(1282, 22)
    pyautogui.click()

#the end
