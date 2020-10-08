from PsychoTest_Classes import PsychoTest_Classes
import requests
import json
import os
from pathlib import Path
import time
import datetime
from json.decoder import JSONDecodeError

os.system("title Psychometry Analyser")
def createLocalDBFolder():#Creates on call home folder and path object of it ,in this folder all data is been stored.
    LocalDBFolder = Path.home() / Path("LocalDB")#Path object , for cross-platform directory path handling.
    LocalDBFolder.mkdir(exist_ok=True) #Creates the Folder,if folder exists it will ignore the exception and will do nothing.
    return LocalDBFolder # Returns Home Folder Path object .

def dateHandler():
    tempDate = datetime.datetime(int(input("\nEnter the year : ")),int(input("\nEnter the month : ")),int(input("\nEnter the day : ")))
    print("This the date you have entered : ",str(tempDate))
    if input("Is it the correct ? If no enter 'no', else enter any key. : ") == "no":
        return dateHandler()
    return tempDate

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
    if Main_LocalDB_Path.exists() and Main_LocalDB_Path.is_file() and Main_LocalDB_Path.stat().st_size > 0:
        with Main_LocalDB_Path.open("r") as File:
            try:
                Main_LocalDB = json.load(File)
            except JSONDecodeError as err:
                print(f"ERROR: {err}")
                print("Local database file exist.\nBut for some reason it's not a valid JSON document.\nPlease contact FXP Psychometry forum management for help.")
                
    Databases["Main_LocalDB"] = Main_LocalDB
    Databases["onlineDB"] = onlineDataBase
    return Databases,Main_LocalDB_Path

def shotdown(Main_LocalDB,Main_LocalDB_Path):
    try:
        with Main_LocalDB_Path.open("w") as Main_LocalDB_File:
            json.dump(Main_LocalDB, Main_LocalDB_File, indent=4)
            return "Successfully saved local database to file."
    except:
        print("ERROR: shotdown raised an error!!!\nFailed to save LocalDB to file!!!\nPLEASE CONTACT IMMEDIATELY FXP PSYCHOMETRY MANAGEMENT!!!")
        return "FAILED SAVING LOCAL DATABASE TO FILE!"


def ADDmode(Databases):
    open_message = """

    ##################################################################
    ##################################################################

    Welcome to 'Add new Test' option!
    ---------------------------------

    Here you will be able to upload a new test to the system.
    Have it checked and analysed!
    ##################################################################
    
    """
    print(open_message)
    if input("If you wish to return to the Main Menu, and not to continue in this option.\nEnter the digit 0 , else Enter any other key. : ") == "0":
        return "CANCEL"
    newTestObject = PsychoTest_Classes.PsychoTest_test(input("Enter a name of your choice for your test. : "))
    print("\n"+"Next you will be adding new chapters to your test."+"\n"+"-"*30)
    inerState = "yes"
    while inerState == "yes":
        print("\n"+"New chapter:"+"\n"+"-"*15)
        typeOfChapter = input("Enter the type of this chapter.\nEnter either 'language', 'math', or 'english'. Of course without any commas. : ")
        numberOfChapter = input("Enter the number ID of the chapter, like in the pdf of the National Center, MALO.\nFor example each published test/pdf, has in order, language 1 and language 2, math 1 and math 2, and english 1 and english 2.\nThese 1 and 2's are the ID of the chapter.\nJust enter 1 or 2. : ")
        periodOfChapter = input("Enter the period of the test/pdf, the chapter is from.\nFor example, 'July', the month the test was, if it's from before 2018.\nOr enter the season, for examle, 'Winter', like in 'Winter 2019', just without the year please. : ")
        yearOfChapter = input("Enter the year of the test/pdf, the chapter is from : ")
        tempChapter = PsychoTest_Classes.PsychoTest_chapter(typeOfChapter, numberOfChapter, periodOfChapter, yearOfChapter)
        tempChapter.enterAnswers()
        print("This is the chapter you have entered: ")
        print(tempChapter)
        
        while input("Are all the answers that had been entered are correct? If no enter 'no'. : ") == "no":
            tempChapter.modifyAnswers()
            print("This is the chapter you have entered: ")
            print(tempChapter)
            
        print(newTestObject.addChapter(tempChapter))
        inerState = input("Do you want to add another chapter? If yes enter 'yes', else Enter any key. : ")
    
    print("\n"+"-"*30+"\n"+"Analysing test....."+"\n"+"-"*15)
    print(newTestObject.check_test(Databases["onlineDB"]))
    print("#"*40)
    print("Uploading test results and it's analysis to local database.")
    if not newTestObject.intoDataBase(Databases["Main_LocalDB"]):
        print("ERROR: In intoDataBase(), Local database in Databases isn't a Dictionary instance/type. ")
        print("Please contact FXP Psychometry management.")
    final_message = f"""
#####################################################################################
Finished and successfuly uploaded the test that was named {newTestObject.nameOfTest}.
Which was created at {newTestObject.creationOfTestObject_DateTime}.
#####################################################################################

Returning to Main Menu.............
#####################################################################################
#####################################################################################

"""
    return final_message


def VIEWmode(DataBases):
    open_message = """

    ##################################################################
    ##################################################################

    Welcome to 'View Statistics and Documentations' option!
    ---------------------------------

    Here you will be able to view all the statistics and documentations on
    test you have enterd into the system till now.
    ##################################################################
    
    """
    print(open_message)
    if (not isinstance(DataBases,dict)) or (not isinstance(DataBases["Main_LocalDB"],dict)):
        print("ERROR:DataBases or Local database in Databases isn't a Dictionary instance/type. ")
        print("Please contact FXP Psychometry management.")
        return "CANCEL"
    if DataBases["Main_LocalDB"] == {}:
        print("You have 0 tests in the local database, therefore you are being returned to the main menu.")
        return "CANCEL"
    if input("If you wish to return to the Main Menu, and not to continue in this option.\nEnter the digit 0 , else Enter any other key. : ") == "0":
        return "CANCEL"
    view_mode_firstMenu = """
    _______________________________________________________________
    You can calculate statistics and view of different time spans.
    You would be able to choose from when it's releavent for you.
    And untill when it's releavent for you.
    ---------------------------------------------------------------

    The dates you would be asked to enter would be in numbers.
    For example:
    1/1/2020
    

    """
    print(view_mode_firstMenu)
    print("Now enter the date of from when it's releavent for you. :\n")
    start_timeSpan = dateHandler()
    print("Now enter the date of untill when it's releavent for you. :\n")
    if input("Would you like it to be untill now, in time also?\nFor example if you had enterd a test today, and you wanted it to be included.\nEnter 'yes' for untill now, in date and time, else enter any key. : ") == "yes":
        end_timeSpan = datetime.datetime.now()
    else:
        end_timeSpan = dateHandler()
    dictOfReleaventOfTests = {}
    for nameOfTest in DataBases["Main_LocalDB"]:
        for datetime_index in DataBases["Main_LocalDB"][nameOfTest]:
            datetime_index_as_datetime_object = datetime.datetime.fromisoformat(datetime_index)
            if start_timeSpan <= datetime_index_as_datetime_object <= end_timeSpan:
                dictOfReleaventOfTests[datetime_index] = PsychoTest_Classes.PsychoTest_test.fromDataBase(nameOfTest,datetime_index,DataBases["Main_LocalDB"])
    numberOfTests = len(dictOfReleaventOfTests)
    numberOfChaptersByType = {"language":0,"math":0,"english":0}
    sumOfCorrectAnswersOfChaptersByType = {"language":0,"math":0,"english":0}
    for timeIndex in dictOfReleaventOfTests:
        for chapter in dictOfReleaventOfTests[timeIndex].chapters:
            numberOfChaptersByType[chapter.typeOfChapter] += 1
            sumOfCorrectAnswersOfChaptersByType[chapter.typeOfChapter] += int(dictOfReleaventOfTests[timeIndex].test_results[chapter.year][chapter.period][chapter.typeOfChapter][chapter.numberOfChapter]["Result"]["numberOfCorrectAnswers"].split("/")[0])
    time.sleep(2)
    firstAnalysis = f"""
     ####################################################################
     First Analysis:
     ---------------
     Number of tests in this analysis: {numberOfTests}
     ---------------------------------------------------
     

     """
    for TYPE in numberOfChaptersByType:
        if numberOfChaptersByType[TYPE] < 1:
            firstAnalysis += f"""
     {TYPE}:
     ---------

     Number of {TYPE} chapters: {numberOfChaptersByType[TYPE]}
     
     Average {TYPE} chapter preformance: 0 / {PsychoTest_Classes.ChapterTypes[TYPE]}
     Average {TYPE} chapter success rate: 0%
     -----------------------------------------------------------------------------------------------------------------------------------------------------------------

     """
        else:
            firstAnalysis += f"""
     {TYPE}:
     ---------

     Number of {TYPE} chapters: {numberOfChaptersByType[TYPE]}
     
     Average {TYPE} chapter preformance: {sumOfCorrectAnswersOfChaptersByType[TYPE]/numberOfChaptersByType[TYPE]} / {PsychoTest_Classes.ChapterTypes[TYPE]}
     Average {TYPE} chapter success rate: {100*(sumOfCorrectAnswersOfChaptersByType[TYPE]/numberOfChaptersByType[TYPE]) / PsychoTest_Classes.ChapterTypes[TYPE]:.2f}%
     -----------------------------------------------------------------------------------------------------------------------------------------------------------------

     """
    print(firstAnalysis+"\n"+"#"*30)
    time.sleep(2)
    if input("Would you like to see brief of the preformance for each test?\nEnter 'yes' to do so, else enter any key. : ") == "yes":
        print("#"*30+"\n")
        for timeIndex in sorted(dictOfReleaventOfTests.keys()):
            print(dictOfReleaventOfTests[timeIndex])
            if input("Would you like to see full analysis of test?\nEnter 'yes' to do so, else enter any key. : ") == "yes":
                print("\n"+"-"*30)
                print(dictOfReleaventOfTests[timeIndex].check_test(DataBases["onlineDB"]))
                print("\n"+"-"*30)
            print("#"*30+"\n")
            time.sleep(3)
    final_message = f"""
#####################################################################################
#####################################################################################

Returning to Main Menu.............
#####################################################################################
#####################################################################################

"""
    return final_message




def MANAGEmode(DataBases):
    print("MANAGEmode(DataBases)")

def DELETEmode(DataBases):
    print("DELETEmode(DataBases)")



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
print(PsychoTest_Classes.logo)
time.sleep(1)
print(start_message)
time.sleep(2.5)
DataBases,Main_LocalDB_Path = startUp()

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
       2) View Statistics and Documentations of tests in your Local database.
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
        print(ADDmode(DataBases))
    elif user_selected_this_option == "2":
        print(VIEWmode(DataBases))
    elif user_selected_this_option == "3":
        MANAGEmode(DataBases)
    elif user_selected_this_option == "4":
        DELETEmode(DataBases)
    elif user_selected_this_option == "0":
        runMenu = False
    time.sleep(2)
print("#"*60+"\n"+"#"*60+"\n"+shotdown(DataBases["Main_LocalDB"],Main_LocalDB_Path)+"\n"+"#"*60+"\n"+"#"*60+"\n")
exit_message = "#"*60+"\n"+"#"*60+"\n"+"""
Existing the application.......
Good Bye and thanks for using the application.
*Credit to @gilbear and FXP Psychometry managment.*

"""+"#"*60+"\n"+"#"*60+"\n"

print(exit_message)
print(PsychoTest_Classes.logo)

input("Press any key to exit and close window ...")

