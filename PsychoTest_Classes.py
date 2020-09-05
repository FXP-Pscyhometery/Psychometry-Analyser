import datetime

ChapterTypes = { "language": 23,"math": 20,"english": 22 } # a dictionary to set the diffrent types of Psychometry chapters


class PsychoTest_chapter: #A class for a psychometry generic-type chapter
    
    def __init__(self, typeOfChapter, numberOfChapter, period, year, q_a = None): #Constructor
        self.typeOfChapter = typeOfChapter
        self.numberOfChapter = numberOfChapter
        self.period = period
        self.year = year
        if q_a == None:
            self.q_a = [0]*ChapterTypes[typeOfChapter]
        else:
            self.q_a = q_a

    def enterAnswers(self): # A function, that lets the user enter his answers to the chapter Object.
        print("Entered blank/new chapter state, enter answers now:")
        for i in range(len(self.q_a)):
            self.q_a[i]= int(input(f"Answer to question number {i+1}: "))
        print("Finished entering answers to this chapter!")

    def modifyAnswers(self): #
        print("Entered chapter modify state:")
        Times = int(input("How many q&a you want to modify?: "))
        for i in range(Times):
            q= int(input("Enter number of question: "))
            a= int(input("Enter number of answer: "))
            self.q_a[q-1]=a
        print("Finished modifying!")
    def __repr__(self): #Debuging form of repersantation of Chapter object
        return f" Type:{self.typeOfChapter}, Num.{self.numberOfChapter}, Edition{self.period},{self.year} : \n { self.q_a } \n"
    def __str__(self): #User form of repersantation of Chapter object
        answer = f" Psychometry {self.typeOfChapter} chapter , Number: {self.numberOfChapter}, from the {self.period} {self.year} Edition: \nQuestions and Answers:\n"+"#"*40+"\n"
        
        for i in range(len(self.q_a)):
            answer += f"| Question number {i+1}| Answer number {self.q_a[i]} |\n"
        answer+= "#"*40
        return answer
#    def toDictForm(self,oldDataBase,mode): # Takes a given Chapter Object and returns a new dictonary rperesentation of the object. Used for seralization..
#        if mode == "ADD":
#            if not self.year in oldDataBase.keys():
#                oldDataBase[self.year] = {}
#            if not self.period in oldDataBase[self.year].keys():
#                oldDataBase[self.year][self.period] = {}
#            if not self.typeOfChapter in oldDataBase[self.year][self.period].keys():
#                oldDataBase[self.year][self.period][self.typeOfChapter] = {}
#            if i.numberOfChapter in oldDataBase[self.year][self.period][self.typeOfChapter].keys():
#                print("This chapter already exist. Please go to MODIFY mode, to fix the wanted chapter answers in the database if needed.")
#            else:
#                oldDataBase[self.year][self.period][self.typeOfChapter][self.numberOfChapter] = self.q_a

        
#    def reCreate(self,typeOfChapter,numberOfChapter,period,year,q_a): # Takes a given dictionary and create/restore an object by it. Restoring from seralization.
#        answer =  cls(typeOfChapter,numberOfChapter,period,year)
#        answer.q_a = q_a
#        return answer
    def compareWith_q_a_excluded(self, Chapter1): #When you want to check if an Chapter obj is the same of another, but not checking the q_a.
        if (Chapter1 == None) or (not isinstance(Chapter1,cls)):
            return False
        return (self.typeOfChapter==Chapter1.typeOfChapter) and (self.numberOfChapter==Chapter1.numberOfChapter) and (self.period==Chapter1.period) and (self.year==Chapter1.year)
    def is_q_a_Empty(self): # Returns True if the answers of the chapter obj is empty or if the chapter is new. Else, of course returns False.
        return self.q_a == [0]*ChapterTypes[self.typeOfChapter]

#class PsychoTest_test:
#
#    def __init__(self, nameOfTest):
#        self.chapters  = {}
#        self.nameOfTest = nameOfTest
#        self.creationOfTestObject_DateTime = datetime.datetime.now()
#    def addChapter(self,newChapter = PsychoTest_chapter()):
#        if not isinstance(newChapter, PsychoTest_chapter):
#            return "Not Added, you have not used an argument that is the correct type of Object or have entered None."
#        if newChapter.is_q_a_Empty():
#            newChapter.enterAnswers()
#        if self.chapters != {}:
#            for i in self.chapters:
#                if newChapter.compareWith_q_a_excluded(i):
#                    print(f"You have this chapter already in this Test, that named {self.nameOfTest}.")
#                    if input("Would you liked to replace the previous chapter? Enter yes or no: ").lower() == "yes":
#                        i.q_a = newChapter.q_a
#                        return "Old Chapter was replaced."
#                    elif input("Would you liked to modify the previous chapter's answers only? Enter yes or no: ").lower() == "yes":
#                        i.modifyAnswers()
#                        return "Old Chapter was modified."
#                    return
#        return
                    
                        


