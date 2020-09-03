import json
import PsychoTest_Classes
import requests
oldDataBase = {}#requests.get()

Start_text = """
Welcome to management app! Credit to @gilbear
#############################################

Here you will be able to create a new DB for the Psychometery results.
You will be able to download the current DB from the github, and to edit the copy at your system.
When you finish editing, you will be exited from the program.
Then you just either upload by yourself upload the new Datebase version, or you send me (Gilbear) the new version, and I would upload for you.

Let's get started!!!!
#############################################

"""

print(Start_text)

print("What would you like to do? If you would like to add a new test/chapter to the offical results, enter 'ADD'.")
state = input()
while state in ["ADD","REMOVE","MODIFY"]:
    if state == "ADD":
        print("Welcome to ADD mode! For each chapter, you will be asked to enter releavent data.")
        inerState = "yes"
        tempListOfChapters = []
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
            tempListOfChapters.append(tempChapter)
            inerState = input("Do you want to add another chapter? If yes enter 'yes', else press any key. : ")
        #with open("DataBase.json","w") as newDataBase:
        for i in tempListOfChapters:
            if not i.year in oldDataBase.keys():
                oldDataBase[i.year] = {}
            if not i.period in oldDataBase[i.year].keys():
                oldDataBase[i.year][i.period] = {}
            if not i.typeOfChapter in oldDataBase[i.year][i.period].keys():
                oldDataBase[i.year][i.period][i.typeOfChapter] = {}
            if i.numberOfChapter in oldDataBase[i.year][i.period][i.typeOfChapter].keys():
                print("This chapter already exist. Please go to MODIFY mode, to fix the wanted chapter answers in the database if needed.")
            else:
                oldDataBase[i.year][i.period][i.typeOfChapter][i.numberOfChapter] = i.q_a
        print("Finished adding the new chapters to the new DataBase. Exiting current mode...")

    state = input("Which mode would you like to enter now? Enter like before, 'ADD' or 'MODIFY' or 'REMOVE'. : ")


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
exitV = input("press any key to exit: ")


            
