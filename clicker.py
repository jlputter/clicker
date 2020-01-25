import xml.etree.ElementTree as ET
import sys
import queue
import random

class TF:
    text=""
    answer=""
    value=1
    def ask(self):
        print("True or False!")
        val=input(self.text)
        if(val.lower()==self.answer.lower()):
            print("Correct!\n")
        else:
            print("Incorrect!\n")
            
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
            print("Correct!\n")
        else:
            print("Incorrect!\n")
            
class Blank:
    text=""
    answer=""
    value=1
    def ask(self):
        print("Fill in the blank!")
        val=input(self.text)
        if(val.lower()==self.answer.lower()):
            print("Correct!\n")
        else:
            print("Incorrect!\n")
            
class Matching:
    text=""
    pair={}
    answer=[]
    value=1
    def ask(self):
        print("Matching!")
        print(self.text)
        for idx, i in enumerate(self.pair):
            print("%d. %s"%(idx+1,i))
        for i in self.answer:##Change this to print randomly
            print(i)
        for i in self.answer:##also print randomly
            print({i})
            
def XMLToTree(xmlfile):
    tree = ET.parse(xmlfile)
    return tree

def parseQuiz(tree):
    root=tree.getroot()
    questions= queue.Queue()
    for question in root.findall('./question'):
        if(question.attrib['category']=="tf"):#TRUE FALSE
            newQuestion=TF()
            for child in question:
                if(child.tag=="text"):
                    newQuestion.text=child.text
                elif(child.tag=="answer"):
                    newQuestion.answer=child.text
            questions.put(newQuestion)           
        elif(question.attrib['category']=="mc"):#MULTIPLE CHOICE
            newQuestion=MC()
            i=0
            for child in question:
                if(child.tag=="text"):
                    newQuestion.text=child.text
                elif(child.tag=="answer"):
                    newQuestion.answer=child.text
                elif(child.tag=="option"):
                    newQuestion.option.insert(i, child.text)
                    ++i
            questions.put(newQuestion)
        elif(question.attrib['category']=="blank"):#BLANK 
            newQuestion=Blank()
            for child in question:
                if(child.tag=="text"):
                    newQuestion.text=child.text
                elif(child.tag=="answer"):
                    newQuestion.answer=child.text
            questions.put(newQuestion)
        elif(question.attrib['category']=="matching"):#MATCHING
            newQuestion=Matching()
            i=0
            for child in question: 
                if(child.tag=="text"):
                    newQuestion.text=child.text
                elif(child.tag=="pair"):
                    tempOption=""
                    tempAnswer=""
                    for match in child:
                        if(match.tag=="option"):
                            tempOption=match.text
                        elif(match.tag=="answer"):
                            tempAnswer=match.text
                            newQuestion.answer.insert(i, tempAnswer)
                            ++i
                    newQuestion.pair[tempOption]=tempAnswer
            questions.put(newQuestion)
        else:
            print("Question type not found")
            sys.exit()

    return questions

def main():
    tree=XMLToTree("./quiz1.xml")
    questions= parseQuiz(tree)
    for i in range(questions.qsize()):
        questions.get().ask()

main()
