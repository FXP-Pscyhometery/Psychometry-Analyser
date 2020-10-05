import PsychoTest_Classes
import requests
import json
import os
from pathlib import Path
import time

def createLocalDBFolder():#Creates on call home folder and path object of it ,in this folder all data is been stored.
    LocalDBFolder = Path("LocalDB")#Path object , for cross-platform directory path handling.
    LocalDBFolder.mkdir(exist_ok=True) #Creates the Folder,if folder exists it will ignore the exception and will do nothing.
    return LocalDBFolder # Returns Home Folder Path object .

def startUp():
    Databases = {}
    response = requests.get("https://raw.githubusercontent.com/FXP-Pscyhometery/Psychomectry-Analysis-Documentation/master/DataBase.json")
    if response.status_code != 200:
        print("ERROR: Failed to fetch the DataBase from it's online source. HTTP GET Request failed, Status code is not 200.")
        print("Please contact and report to FXP Psychometry management about the ERROR. Exiting now....")
        return "EXIT"
    else:
        try:
            onlineDataBase = response.json()
        except:
            print("ERROR: Failed to fetch the DataBase from it's online source. Response isn't a JSON file.")
            print("Please contact and report to FXP Psychometry management about the ERROR. Exiting now....")
            return "EXIT"
    LocalDBFolder = createLocalDBFolder()
    Main_LocalDB_Path = LocalDBFolder / "main.json"
    Main_LocalDB = {}
    if Main_LocalDB_Path.exists():
        with Main_LocalDB_Path.open("r") as File:
            Main_LocalDB = json.load(File)
    Databases["Main_LocalDB"] = Main_LocalDB
    Databases["onlineDB"] = onlineDataBase
    return Databases


def ADDmode(Databases):
    inerState = "yes"
    while inerState == "yes":
        print("New chapter:")
        typeOfChapter = input("Enter the type of this chapter. Enter either 'language', 'math', or 'english'. Of course without any commas. : ")
        numberOfChapter = input("Enter the number ID of the chapter, like in the pdf of the National Center, MALO. For example each published test/pdf, has in order, language 1 and language 2, math 1 and math 2, and english 1 and english 2. These 1 and 2's are the ID of the chapter. Just enter 1 or 2. : ")
        periodOfChapter = input("Enter the period of the test/pdf, the chapter is from. For example, 'July', the month the test was, if it's from before 2018. Or enter the season, for examle, 'Winter', like in 'Winter 2019', just without the year please. : ")
        yearOfChapter = input("Enter the year of the test/pdf, the chapter is from : ")
        tempChapter = PsychoTest_Classes.PsychoTest_chapter(typeOfChapter, numberOfChapter, periodOfChapter, yearOfChapter)
        tempChapter.enterAnswers()
        print("This is the chapter you have entered: ")
        print(tempChapter)
        finishedWithChapter = input("Are all the answers that had been entered are correct? If no enter 'no'. : ")
        while finishedWithChapter == "no":
            tempChapter.modifyAnswers()
            print("This is the chapter you have entered: ")
            print(tempChapter)
            finishedWithChapter = input("Are all the answers that had been entered are correct? If no enter 'no'. : ")
        tempTest.addChapter(tempChapter)
        inerState = input("Do you want to add another chapter? If yes enter 'yes', else press any key. : ")

def VIEWmode(DataBases):
    print("VIEWmode(DataBases)")

def MANAGEmode(DataBases):
    print("MANAGEmode(DataBases)")

def DELETEmode(DataBases):
    print("DELETEmode(DataBases)")


logo = """
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
 .mmmmmmd/.hmm+   +mms `dmmmmdhs-       -mmmmmdho`  -sdmNNmd`:dmd`   ymd-  -sdmNNmd` +md/    `mmh    :sdNNNdy/    ymmmy     :mmmd.  ymmmmmdy hmdmmmmmmd+ ommmdddy+` smds   .dmh`             
 .MMm////. .mMM/ oMMs  `MMN:/oNMM:      :MMh:/sMMN.:MMm/--/o` +MMd` sMM/ .dMMh+///o` oMM+    `MMN  `dMMh+//yMMm.  mMNMM+   `NMNMM.  mMM+///: ://oMMm///- yMMo:/hMMh  hMM+ `mMm.              
 .MMd       `hMMyMM+   `MMm   yMM+      :MMy  `NMM-:MMNs:`     +MMyoMM/  dMM+        oMMs::::/MMN  hMMo     oMMh  mMdyMN.  yMhdMM.  mMM-...`    -MMd     yMM:  oMMy  `hMM/dMm.               
 .MMMMMMM    `NMMMs    `MMMhhmMMy`      :MMmhhNMN+  -smMMMd+    +MMMM/  `MMM`        oMMMMMMMMMMN  NMM-     -MMN  mMd`mMd /MN`dMM.  mMMMMMM+    -MMd     yMMNmNMh/    `hMMMm`                
 .MMd....   -mMmsMMs   `MMN++/:`        :MMd++/-       `:mMMo    yMMo    mMMo        oMM+    `MMN  hMMs     sMMy  mMd -MMsNM: dMM.  mMM.        -MMd     yMMo:hMNo     `NMM.                 
 .MMd      /MMm. +MMd` `MMm             :MMy       /ho//+mMM/    sMM+    -mMMmsoosd. oMM+    `MMN  `hMMdsosdMMy`  mMd  oMMMs  dMM.  mMMsoooo    -MMd     yMM:  oMMh.    NMM`                 
 .hho     :hhy`   /hhs``yhs             -hh+       -shdddho-     /hh:      :shdddhs` /hh:    `hhy    -oydddy+.    shs   shy`  ohh.  shhhhhhy`   .hhs     +hh-   :hhs`   yhy`                 
://////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////-             
.------------------------------------------------------------------------------------------------------------------------------------------------------------------------------`             
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                
"""
start_message = """
#####################################################################



Welcome to FXP's Psychometry simulations and tests management application!!!!
Here you will be able to document, to check answers and a brife investigate chapters.
You will also be able to have statistics!!!

Credit to @gilbear and Psychometry forum managment!!

#####################################################################
"""
print("Please change to maximum window")
time.sleep(4)
print(logo)
time.sleep(1)
print(start_message)
time.sleep(2.5)
DataBases = startUp()
if DataBases == "EXIT":
    exit()
Main_message = """
MAIN MENU:
---------
      In the following lines, the options/Menu will be shown.
      To choose an option, enter the digit that is shown on the left of each option to select it.
      #
      #
      #
      #
      1) Add a new test.
        -----------------
        ( This option will transfer you to the adding system, where you can add a test you had solved.)
        -----------------------------------------------------------------------------------------------
       #
       #
       #
       #
       2) See Statistics and Documentations of tests in your Local database.
          -----------------------------------------------
          (This option will transfer you to the statitics, documentations and results of all the tests you have enterd here before.)
          -----------------------------------------------------------------------------------------------------------------
        #
        #
        #
        #
        3) Manage existing tests in the system database.
           ------------------------------------------------------------
           (This option is for if you want to manage/edit/check/fill a previous enterd test from the database.)
           ----------------------------------------------------------------------------------
        #
        #
        #
        #
        4) Delete tests from the database.
           -------------------------------
           (This option will let you delete tests you have entered in the system before.)
           ------------------------------------------------------------------------------
        #
        #
        #
        #
        0) Exit the program.
           -----------------
        #
        #
        Please enter your choice in the next line.
        #######################################################################################
"""

runMenu = True
while runMenu:
    print(Main_message)
    user_selected_this_option = input("Enter here the option you want to proceed with. Remember, enter the digit! : ")
    if user_selected_this_option == "1":
        ADDmode(DataBases)
    elif user_selected_this_option == "2":
        VIEWmode(DataBases)
    elif user_selected_this_option == "3":
        MANAGEmode(DataBases)
    elif user_selected_this_option == "4":
        DELETEmode(DataBases)
    elif user_selected_this_option == "0":
        runMenu = False

exit_message = "#"*60+"\n"+"#"*60+"\n"+"""
Existing the application.......
Good Bye and thanks for using the application.
*Credit to @gilbear and FXP Psychometry managment.*
"""

print(exit_message)
print(logo)

input("Press any key to exit and close window ...")

