import xml.etree.ElementTree as ET
import sys
import queue

class TF:
    text=""
    answer=""
    value=1
    def ask(self):
        print("True or False?")
        val=input(self.text)
        if(val==self.answer):
            print("Correct!")
        else:
            print("Incorrect!")
class MC:
    text=""
    option=[]
    answer=""
    value=1
    def ask(self):
        print("Multiple Choice! Type the correct answer")
        print(self.text)
        for i in self.option:
           print(i)
        
        
class Blank:
    text=""
    answer=""
    value=1
    def ask(self):
        print("Fill in the blank")
        
class Matching:
    text=""
    option=[]
    answer={}
    value=1
    def ask(self):
        print("Matching")

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
        elif(question.attrib['category']=="mc"):#MULTIPLE CHOICE//Not working yet, check
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
                print("blank")
            questions.put(newQuestion)
        elif(question.attrib['category']=="matching"):#MATCHING
            newQuestion=Matching()
            for child in question: 
                print("matching")
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

#TODO, get it to work
#I think True False is working, rest are not finished yet
#unhardcode the xml file reference
#add failure handling in case of file/question type not found

#item.attrib gets you {'category': 'tf'}
#child.tag gets you text, answer, option
#child.text gets The sky is blue, Carmello

