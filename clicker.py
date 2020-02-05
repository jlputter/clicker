import xml.etree.ElementTree as ET
import sys
import queue
import random
questionCategories=["tf","mc","blank","matching"]


class Player:
    def __init__(self, name):
        self.name = name
    score=0

class TF:
    text=""
    answer=""
    value=1
    def ask(self):
        print("True or False!")
        val=input(self.text)
        if(isTF(val)==self.answer.lower()):
            correct()
            return self.value
        else:
            incorrect()
            return 0

    def parse(self, question):
        for child in question:
            if(child.tag=="text"):
                self.text=child.text
            elif(child.tag=="answer"):
                self.answer=child.text
            elif(child.tag=="value"):
                self.value=int(child.text)
        return self

class MC:
    text=""
    option=[]
    answer=""
    value=1
    def ask(self):
        print("Multiple Choice! Type the correct answer")
        for idx, i in enumerate(self.option):
           print("%d. %s"%(idx+1,i))
        val=input(self.text)
        if(val.lower()==self.answer.lower()):
            correct()
            return self.value
        else:
            incorrect()
            return 0
        
    def parse(self, question):
        i=0
        for child in question:
            if(child.tag=="text"):
                self.text=child.text
            elif(child.tag=="answer"):
                self.answer=child.text
            elif(child.tag=="option"):
                self.option.insert(i, child.text)
                ++i
            elif(child.tag=="value"):
                self.value=int(child.text)
        return self

            
class Blank:
    text=""
    answer=""
    value=1
    def ask(self):
        print("Fill in the blank!")
        val=input(self.text)
        if(val.lower()==self.answer.lower()):
            correct()
            return self.value
        else:
            incorrect()
            return 0

    def parse(self, question):
        for child in question:
            if(child.tag=="text"):
                self.text=child.text
            elif(child.tag=="answer"):
                self.answer=child.text
            elif(child.tag=="value"):
                self.value=int(child.text)
        return self

            
class Matching:
    text=""
    pair={}
    option=[]
    answer=[]
    value=1
    def ask(self):
        isCorrect=True
        print("Matching!")
        print(self.text)
        for idx, i in enumerate(self.option):
            print("%d. %s"%(idx+1,i))
        print("Your options are:")
        for i in range(0, len(self.answer)):
            print(self.answer.pop(random.randrange(len(self.answer))))
        print()
        for i in range(0, len(self.option)):
            rand=self.option.pop(random.randrange(len(self.option)))
            val=input("%s matches with "% rand)
            if(val.lower()==self.pair.get(rand).lower()):
                correct()
            else:
                incorrect()
                isCorrect=False
        if(isCorrect):
            return self.value
        else:
            return 0

    def parse(self, question):
        i=0
        j=0
        for child in question: 
            if(child.tag=="text"):
                self.text=child.text
            elif(child.tag=="pair"):
                tempOption=""
                tempAnswer=""
                for match in child:
                    if(match.tag=="option"):
                        tempOption=match.text
                        self.option.insert(j, tempOption)
                        ++j
                    elif(match.tag=="answer"):
                        tempAnswer=match.text
                        self.answer.insert(i, tempAnswer)
                        ++i
                self.pair[tempOption]=tempAnswer
            elif(child.tag=="value"):
                self.value=int(child.text)
        return self
       
def XMLToTree(xmlfile):
    tree = ET.parse(xmlfile)
    return tree

def parseQuiz(tree):
    root=tree.getroot()
    allQuestions= queue.Queue()
    for unparsedQuestion in root.findall('./question'):
        if(unparsedQuestion.attrib['category']=="tf"):#TRUE FALSE
            newQuestion=TF()
            newQuestion.parse(unparsedQuestion)
            allQuestions.put(newQuestion)          
        elif(unparsedQuestion.attrib['category']=="mc"):#MULTIPLE CHOICE
            newQuestion=MC()
            newQuestion.parse(unparsedQuestion)
            allQuestions.put(newQuestion)
        elif(unparsedQuestion.attrib['category']=="blank"):#Fill In Blank
            newQuestion=Blank()
            newQuestion.parse(unparsedQuestion)
            allQuestions.put(newQuestion)
        elif(unparsedQuestion.attrib['category']=="matching"):#MATCHING
            newQuestion=Matching()
            newQuestion.parse(unparsedQuestion)
            allQuestions.put(newQuestion)
        else:
            print("Question type not found")
            sys.exit()
    return allQuestions

def isTF(reponse):
    if(reponse.lower()=="t") or (reponse.lower()=="true"):
        return"true"
    elif(reponse.lower()=="f") or (reponse.lower()=="false"):
        return"false"
    return"wrongo"

def correct():
    print("Correct!\n")
def incorrect():
    print("Incorrect!\n")

def runQuiz(questions, player):
    for i in range(questions.qsize()):
        player.score+=questions.get().ask()
    print("%ss score=%d"% (player.name, player.score))

def main():
    tree=XMLToTree("./quiz1.xml")
    questions= parseQuiz(tree)
    p1=Player("Ryne")
    runQuiz(questions, p1)

main()
