#Made by @gilbear and @gilkzxc
import json
import time
from PsychoTest_Classes import PsychoTest_Classes
import requests
import os
os.system("title Psychometry Analyser - Management")
def ADDmode(oldDataBase): # Function that collects information, answers, and anything to create and add to the temporary DataBase.
    print("Welcome to ADD mode! For each chapter, you will be asked to enter releavent data.")
    inerState = "yes"
    tempListOfChapters = []
    while inerState == "yes":
        print("\n"+"New chapter:"+"\n"+"-"*15)
        typeOfChapter =  PsychoTest_Classes.chapterTypeGenerator()
        numberOfChapter = input("Enter the number ID of the chapter, like in the pdf of the National Center, MALO.\nFor example each published test/pdf, has in order, language 1 and language 2, math 1 and math 2, and english 1 and english 2.\nThese 1 and 2's are the ID of the chapter.\nJust enter 1 or 2. : ")
        periodOfChapter = input("Enter the period of the test/pdf, the chapter is from.\nFor example, 'July', the month the test was, if it's from before 2018.\nOr enter the season, for examle, 'Winter', like in 'Winter 2019', just without the year please. : ")
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
        tempListOfChapters.append(tempChapter)
        inerState = input("Do you want to add another chapter? If yes enter 'yes', else press any key. : ")
    for i in tempListOfChapters:
            if not i.addingToDataBase(oldDataBase):
                print("This chapter already exist. Please go to MODIFY mode, to fix the wanted chapter answers in the database if needed.")        
    print("Finished adding the new chapters to the new DataBase. Exiting current mode...")

def MODIFYmode(oldDataBase):
    print("Welcome to MODIFY mode! For each chapter, you will be asked to enter releavent data.")
    year = input("Enter the year of the test you wish to edit/modify. : ")
    for period in oldDataBase[year].keys():
        if input(f"Do you wish to modify a chapter/test/pdf on this period, {period}? Enter 'yes' to do so, else any key to continue. : ") == "yes":
            for Type in oldDataBase[year][period].keys():
                if input(f"Do you wish to modify a chapter of this type, {Type}? Enter 'yes' to do so, else any key to continue. : ") == "yes":
                    for i in ["1","2"]:
                        if input(f"Do you wish to modify chapter {i}? Enter 'yes' to do so, else any key to continue. : ") == "yes":
                            temp = PsychoTest_Classes.PsychoTest_chapter(Type,i,period,year,oldDataBase[year][period][Type][i])
                            temp.modifyAnswers()
                            print("This is the result of the chapter you have edited: ")
                            print(temp)
                            finishedWithChapter = input("Are all the answers that had been entered are correct? If no enter 'no'. : ")
                            while finishedWithChapter == "no":
                                temp.modifyAnswers()
                                print("This is the result of the chapter you have edited: ")
                                print(temp)
                                finishedWithChapter = input("Are all the answers that had been entered are correct? If no enter 'no'. : ")
                            oldDataBase[year][period][Type][i] = temp.q_a
    print("Finished editing/modifying the tests and chapters, being updated to the new DataBase. Exiting current mode...")

def DELETmode(oldDataBase):
    print("Welcome to Delete mode! For each chapter/test, you will be asked to enter releavent data.")
    print("Be careful!! This is Delete mode, here you delet data from the DataBase!!! \nBut still, Data will be forever lost only, if the old DataBase file that on GitHub will be replaced with the new Localy created version of the file in the computer. ")
    year = input("Enter the year of the test/chapter you would like to delete. : ")
    if input("Would you like to delet a whole year? Enter 'yes' for yes. : ") == "yes":
        oldDataBase.pop(year)
        if input("Would you like to delete more? (Have you not had enough? :) ) Enter 'yes' to continue be in Delete mode : ") == "yes":
            DELETmode(oldDataBase)
        return
    period = input("Enter the period of the test/chapter you would like to delete. : ")
    if input("Would you like to delet the whole test\period? Enter 'yes' for yes. : ") == "yes":
        oldDataBase[year].pop(period)
        if input("Would you like to delete more? (Have you not had enough? :) ) Enter 'yes' to continue be in Delete mode : ") == "yes":
            DELETmode(oldDataBase)
        return
    Type = input("Enter the type of the chapter you wish to delete. : ")
    if input("Would you like to delet the whole type? Enter 'yes' for yes. : ") == "yes":
        oldDataBase[year][period].pop(Type)
        if input("Would you like to delete more? (Have you not had enough? :) ) Enter 'yes' to continue be in Delete mode : ") == "yes":
            DELETmode(oldDataBase)
        return
    numberOfChapter = input("Enter the ID number , 1 or 2, of the chapter you wish to delete. : ")
    oldDataBase[year][period][Type].pop(numberOfChapter)
    if input("Would you like to delete more? (Have you not had enough? :) ) Enter 'yes' to continue be in Delete mode : ") == "yes":
            DELETmode(oldDataBase)
    print("Finished Deleting the tests and chaptes, being updated to the new DataBase. Exiting current mode...")


start_message = """
Welcome to management app! Credit to @gilbear
#############################################

Here you will be able to create a new DB for the Psychometery results.
You will be able to download the current DB from the github, and to edit the copy at your system.
When you finish editing, you will be exited from the program.
Then you just either upload by yourself upload the new Datebase version, or you send me (Gilbear) the new version, and I would upload for you.

Let's get started!!!!
#############################################

"""

input("Please change to maximum window.\nPress the Enter key to continue.")
print(PsychoTest_Classes.logo)
time.sleep(1)
print(start_message)
time.sleep(2.5)


response = PsychoTest_Classes.OnlineDB_GET_Response
if response.status_code != 200:
    print("Failed to fetch the DataBase from it's online source. HTTP GET Request failed, not 200.")
    if input("Would you like to use a new/blank DataBase? Enter yes for yes, else any key to exit. : ") == "yes":
        oldDataBase = {}
    else:
        exit()
else:
    try:
        oldDataBase = response.json()
    except:
        print("Failed to fetch the DataBase from it's online source. Response isn't a JSON file.")
        if input("Would you like to use a new/blank DataBase? Enter yes for yes, else any key to exit. : ") == "yes":
            oldDataBase = {}
        else:
            exit()
if input("Would like to see DataBase here first? Enter 'yes' to do so. : ") == "yes":
    print(json.dumps(oldDataBase, indent=4))

mainAlgoMessage = """
What would you like to do?
If you would like to add a new test/chapter to the official results, enter 'ADD'.
If you would like to change/update/modify/edit the official results, enter 'MODIFY'.
If you would like to delete tests/chapters from the official results, enter 'DELETE'. 
Enter down below:
"""
print(mainAlgoMessage)
state = input()

while state in ["ADD","DELETE","MODIFY"]:
    if state == "ADD":
        ADDmode(oldDataBase)
    elif state == "MODIFY":
        MODIFYmode(oldDataBase)
    elif state == "DELETE":
        DELETEmode(oldDataBase)
        
    state = input("Which mode would you like to enter now? Enter like before, 'ADD' or 'MODIFY' or 'DELETE'. Or press Enter to contiue to exit. : ")


print("Now creating the new version of the DataBase, which you would need to upload/replace manually later.")
with open("DataBase.json","w") as newDataBase:
    json.dump(oldDataBase, newDataBase, indent=4)

print("The new version of the DataBase was successfuly created!!")

End_text = """

###############################################################################################
Exiting management app!!
Don't forget to replace the updated and new DataBase file with the old one on GitHub.
Don't know how? ask @gilbear or your supervisor or other managers, or read again the guide, if exist...

Exit!
###############################################################################################
"""
print(PsychoTest_Classes.logo)
input("press any key to exit: ")


            
