import PsychoTest_Classes
import requests
import json



start_message = """
#####################################################

Welcome to FXP's Psychometry simulations and tests management application!!!!
Here you will be able to document, to check answers and a brife investigate chapters.
You will also be able to have statistics!!!

Credit to @gilbear and Psychometry forum managment!!

#####################################################################
"""

print(start_message)
res = requests.get("https://raw.githubusercontent.com/FXP-Pscyhometery/Psychomectry-Analysis-Documentation/master/DataBase.json")
ttt = PsychoTest_Classes.PsychoTest_test(input("Enter name of test: "))
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
    ttt.addChapter(tempChapter)
    inerState = input("Do you want to add another chapter? If yes enter 'yes', else press any key. : ")
print("#"*60)
print("Test Analysis:")
print("#"*60)
onlineData = res.json()
ttt.check_test(onlineData)
print("#"*60)
print("Test STR:")
print("#"*60)
print(ttt)


