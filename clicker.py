import xml.etree.ElementTree as ET
import sys

def XMLToTree(xmlfile):
    tree = ET.parse(xmlfile)
    return tree

def parseQuiz(tree):
    root=tree.getroot()
    for question in root.findall('./question'):
        if(question.attrib['category']=="tf"):
            print("True or false")
            for child in question:
                ##if child.
                print("tf") 
        elif(question.attrib['category']=="mc"):
            print("Multiple choice")
            for child in question: 
                print("mc") 
        elif(question.attrib['category']=="blank"):
            print("Fill in the bank")
            for child in question: 
                print("blank") 
        elif(question.attrib['category']=="matching"):
            print("Matching")
            for child in question: 
                print("matching") 
        else:
            print("Question type not found")
            sys.exit()

def main():
    tree=XMLToTree("./quiz1.xml")
    this= parseQuiz(tree)    

main()

