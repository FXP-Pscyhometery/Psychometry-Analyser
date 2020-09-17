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
res = requests.get("https://raw.githubusercontent.com/FXP-Pscyhometery/final_answers_inventory/master/DataBase.json")
a = PsychoTest_Classes.PsychoTest_chapter("language","2","Summer","2020",[1]*23) #Example of chapter.
print(a) 
result = a.checkAnswers(res.json())
print(result["__str__"]["with_actual_correct_answers"])#Example of chapter investigation.



