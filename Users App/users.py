#Made by @gilbear and @gilkzxc
from PsychoTest_Classes import PsychoTest_Classes
import requests
import json
import os
from pathlib import Path
import time
import datetime
from json.decoder import JSONDecodeError
import plotly.express as plotly_express
import plotly.graph_objects as go

os.system("title Psychometry Analyser")
def createLocalDBFolder():#Creates on call home folder and path object of it ,in this folder all data is been stored.
    LocalDBFolder = Path.home() / Path("LocalDB")#Path object , for cross-platform directory path handling.
    LocalDBFolder.mkdir(exist_ok=True) #Creates the Folder,if folder exists it will ignore the exception and will do nothing.
    return LocalDBFolder # Returns Home Folder Path object .

def dateHandler():
    tempDate = datetime.datetime(int(input("\nEnter the year (in YYYY format): ")),int(input("\nEnter the month : ")),int(input("\nEnter the day : ")))
    print("This the date you have entered : ",str(tempDate))
    if input("Is it the correct ? If no enter 'no', else enter any key. : ") == "no":
        return dateHandler()
    return tempDate

def HistogramsGraphGenerator(title,x,y,labels={"x":"x","y":"y"},text=None,hovertemplate=""):
    if not isinstance(x,list):
        print("ERROR: Invalid x argument for graphGenerator.\n x isn\'t a list type.")
        return 
    if not isinstance(y,list):
        print("ERROR: Invalid y argument for graphGenerator.\n y isn\'t a list type.")
        return
    fig = plotly_express.bar(x=x,y=y,labels=labels,title=title,text=text)
    if isinstance(hovertemplate,str) and len(hovertemplate)>0:
        fig.update_traces(hovertemplate=hovertemplate)
    fig.show()
    input("Press the enter key to continue or enter any key : ")
    return


def retrieveTestsByName(DataBases):
    opening_text = """
    _______________________________________________________________
    Tests by name retriever!
    -----------------------------
    Through here you would be able to choose the tests you want,
    through entering their name.

    ---------------------------------------------------------------
    If the name you have entered is incorrect or there isn't a test
    with that name.
    Then no test would be retrieved of course.
    ---------------------------------------------------------------

    """
    print(opening_text)
    nameOfTest = input("Enter the name of the test\s you would like to retrieve. : ")
    if not nameOfTest in DataBases["Main_LocalDB"]:
        print("The name you have entered is wrong\nOr there isn't a test with this name.\nTherefore you retrieve none.")
        return {}
    dictOfReleaventOfTests = {}
    for datetime_index in DataBases["Main_LocalDB"][nameOfTest]:
        dictOfReleaventOfTests[datetime_index] = PsychoTest_Classes.PsychoTest_test.fromDataBase(nameOfTest,datetime_index,DataBases["Main_LocalDB"])
    return dictOfReleaventOfTests

def retrieveTestsByTimeSpan(DataBases):
    opening_text = """
    _______________________________________________________________
    Tests by time span retriever!
    -----------------------------
    Through here you would be able to choose the tests you want,
    through selecting the time span.

    By choosing the begin of the time span, and by choosing the end.
    The test that you would retrieve will be like this:
    Begin time span <= the time a test was created <= End time span.
    ---------------------------------------------------------------

    The dates you would be asked to enter would be in numbers.
    For example:
    1/1/2020
    

    """
    print(opening_text)
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
    if dictOfReleaventOfTests == {}:
        print("The dates you have entered is wrong\nOr there isn't a test between these dates.\nTherefore you retrieve none.")
    return dictOfReleaventOfTests


def startUp():
    Databases = {}
    response = PsychoTest_Classes.OnlineDB_GET_Response
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
        typeOfChapter = PsychoTest_Classes.chapterTypeGenerator()
        numberOfChapter = input("Enter the number ID of the chapter, like in the pdf of the National Center, MALO.\nFor example each published test/pdf, has in order, language 1 and language 2, math 1 and math 2, and english 1 and english 2.\nThese 1 and 2's are the ID of the chapter.\nJust enter 1 or 2. : ")
        periodOfChapter = input("Enter the period of the test/pdf, the chapter is from.\nFor example, 'July', the month the test was, if it's from before 2018.\nOr enter the season, for examle, 'Winter', like in 'Winter 2019', just without the year please. : ")
        yearOfChapter = input("Enter the year of the test/pdf, the chapter is from. In YYYY format. : ")
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
    -------------------------------------------------------

    Here you will be able to view all the statistics and documentations on
    test you have enterd into the system till now.
    ##################################################################
    
    """
    final_message = f"""
#####################################################################################
#####################################################################################

Returning to Main Menu.............
#####################################################################################
#####################################################################################

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
    view_1st_main_message = """
    -------------------------------------------------------------------------

    You can view a few tests or review, you can check all of them, or only one.
    Two options:
    ------------
    1)You can retrieve a specific singulare test by name.
        (If you have entered more than one test with the same name, the system would retrieve and review all of them.)

    OR

    2)You can choose a time span to retrieve all tests you have created/uploaded between the dates you will choose.
        (If you want a specific test, than you can also choose this option.
         Useful, for example, you have forgotten the name of the test,
         or you have a bunch of tests with the same name, and still want a single one.)

    ---------------------------------------------------------------------------------------------------------------

    """
    print(view_1st_main_message)
    dictOfReleaventOfTests = {}
    option = input("Enter the option you would like to go with.\nEnter the digit of each option, '1' for by name, '2' for by between dates. : ")
    if option == "1":
        dictOfReleaventOfTests = retrieveTestsByName(DataBases)
    elif option == "2":
        dictOfReleaventOfTests = retrieveTestsByTimeSpan(DataBases)
    if dictOfReleaventOfTests == {}:
        return final_message
    numberOfTests = len(dictOfReleaventOfTests)
    numberOfChaptersByType = {"language":0,"math":0,"english":0}
    sumOfCorrectAnswersOfChaptersByType = {"language":0,"math":0,"english":0}
    preformanceInTypeByName_and_Date_y = {"language":[],"math":[],"english":[]}
    preformanceInTypeByName_and_Date_x = {"language":[],"math":[],"english":[]}
    testWithSameName = {}
    datetimeIndexies = {"language":[],"math":[],"english":[]}
    for timeIndex in sorted(dictOfReleaventOfTests.keys()):
        tempSum = {"language":0,"math":0,"english":0}
        for chapter in dictOfReleaventOfTests[timeIndex].chapters:
            numberOfChaptersByType[chapter.typeOfChapter] += 1
            tempSum[chapter.typeOfChapter] += int(dictOfReleaventOfTests[timeIndex].test_results[chapter.year][chapter.period][chapter.typeOfChapter][chapter.numberOfChapter]["Result"]["numberOfCorrectAnswers"].split("/")[0])
        for Type in ["language","math","english"]:
            if tempSum[Type]>0:
                tempNameOfTest = dictOfReleaventOfTests[timeIndex].nameOfTest
                if not tempNameOfTest in testWithSameName:
                    testWithSameName[tempNameOfTest] = 1
                else:
                    testWithSameName[tempNameOfTest] += 1
                preformanceInTypeByName_and_Date_x[Type].append(tempNameOfTest+f"-{testWithSameName[tempNameOfTest]}")
                datetimeIndexies[Type].append(timeIndex)
                preformanceInTypeByName_and_Date_y[Type].append(tempSum[Type])
                sumOfCorrectAnswersOfChaptersByType[Type] += tempSum[Type]

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
    print("""

    ------------------------------------------------------------------------------
    Will now open graphs of preformance over time for each type of chapters.
    The graph will help you understand if you are imporving or not over time.
    They will open in you default web browser in a new tab.
    Don't worry the program will wait for you ( you will see :) ).
    It 
    ------------------------------------------------------------------------------

    """)
    for Type in ["language","math","english"]:
        if len(preformanceInTypeByName_and_Date_x[Type])>0 and len(preformanceInTypeByName_and_Date_y[Type])>0:
            labels = {"x":"Date of test","y":"Sum of correct answers in type per test"}
            title = f"Graph of {Type} chapter type's preformance over time"
            hovertemplate="<i>Sum</i>: %{y}<br><b>Name</b>: %{x}<br><b>Date</b>: %{text}"
            HistogramsGraphGenerator(title=title,x=preformanceInTypeByName_and_Date_x[Type],y=preformanceInTypeByName_and_Date_y[Type],labels=labels,text=datetimeIndexies[Type],hovertemplate=hovertemplate)
        else:
            print(f"You don't have in these tests results in this type {Type}.\nSo NO GRAPH FOR YOU! :)")
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

    return final_message




def MANAGEmode(DataBases):
    final_message = f"""
#####################################################################################
#####################################################################################

Returning to Main Menu.............
#####################################################################################
#####################################################################################

"""
    if (not isinstance(DataBases,dict)) or (not isinstance(DataBases["Main_LocalDB"],dict)):
        print("ERROR:DataBases or Local database in Databases isn't a Dictionary instance/type. ")
        print("Please contact FXP Psychometry management.")
        return "CANCEL"
    if DataBases["Main_LocalDB"] == {}:
        print("You have 0 tests in the local database, therefore you are being returned to the main menu.")
        return "CANCEL"
    if input("If you wish to return to the Main Menu, and not to continue in this option.\nEnter the digit 0 , else Enter any other key. : ") == "0":
        return "CANCEL"
    return final_message


def DELETEmode(DataBases):
    open_message = """

    ##################################################################
    ##################################################################

    Welcome to 'Delete tests from the database' option!
    ---------------------------------------------------

    Here you will be able to view all the statistics and documentations on
    test you have enterd into the system till now.

    ALL DELETES HERE ARE IRREVERSIBLE!!!
    ##################################################################
    
    """
    final_message = f"""
#####################################################################################
#####################################################################################

Returning to Main Menu.............
#####################################################################################
#####################################################################################

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
    print("-"*30+"\n"+"To protect you from accidential deletes,\nyou are only able to retrieve tests by name,\nthen you will be asked the exact date/version of test to delete."+"\n"+"-"*30)
    dictOfReleaventTests = retrieveTestsByName(DataBases)
    if dictOfReleaventTests == {}:
        return final_message
    sorted_keys = sorted(dictOfReleaventTests.keys())
    nameOfTest = dictOfReleaventTests[sorted_keys[0]].nameOfTest
    msg = f"""
    ------------------------------------------------------------------------------
    These are the test with this, {nameOfTest}, as their name.

    The following are the dates/versions of all the tests with the same name, as the above.:


    """
    for position in range(len(sorted_keys)):
        msg +=f"""{position}. {sorted_keys[position]}""" +"\n"
    print(msg)
    if input("If you wanted to delete all the tests with the same name.\nEnter the name to confirm you are sure you want to delete them all.\nElse just press the enter key.\nREMEBER THIS IS IRREVERSIBLE\nEnter here :  ") == nameOfTest:
        DataBases["Main_LocalDB"].pop(nameOfTest)
        print("Deleted all the tests with the same name from the local database.")
        return final_message
    try:
        chosenDateToDelete = int(input("Enter the number on the left of the dot, for the test you wish to delete. : "))
    except ValueError:
        print("You have entered an invalid input, you are being returend to main menu.")
        return final_message
    if not chosenDateToDelete in range(len(sorted_keys)):
            print("You have entered an invalid input, you are being returend to main menu.")
            return final_message
    print("You have entered this :",chosenDateToDelete)
    print("The chosen test:\n"+"-"*15)
    print(dictOfReleaventTests[sorted_keys[chosenDateToDelete]])
    options = input("Are you sure you want to delete this test?\nEnter 'yes' if you are, else press the enter key or enter any key. : ")
    if options == "yes":
        DataBases["Main_LocalDB"][nameOfTest].pop(sorted_keys[chosenDateToDelete])
        print("Deleted the chosen test with the chosen name and chosen date from the local database.")
        if DataBases["Main_LocalDB"][nameOfTest] == {}:
            DataBases["Main_LocalDB"].pop(nameOfTest)
        return final_message
    print("***System did not delete anything or failed to do so.***")
    return final_message

    





start_message = """
#####################################################################



Welcome to FXP's Psychometry simulations and tests management application!!!!
Here you will be able to document, to check answers and a brife investigate chapters.
You will also be able to have statistics!!!

Credit to @gilbear and Psychometry forum managment!!

#####################################################################
"""
input("Please change to maximum window.\nPress the Enter key to continue.")

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
           *Only by exiting through this option all changes will be saved.*
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
        print(MANAGEmode(DataBases))
    elif user_selected_this_option == "4":
        print(DELETEmode(DataBases))
    elif user_selected_this_option == "0":
        runMenu = False
    else:
        print("You have entered an invalid input, please enter a vailid input.")
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

