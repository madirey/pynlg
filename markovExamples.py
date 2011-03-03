from MarkovCharacterGenerator import *
import string

def main():
    FILE_NAME = "c:\\documents and settings\\mcaldwell\\desktop\\alice.txt"
    #FILE_NAME = "c:\\dl\\borland\\readme.txt"
    file = open(FILE_NAME)
    textToken = file.read()
    textToken = string.replace(textToken, "\n", " ")
    file.close()

    for i in range(1,10):
        generator = MarkovCharacterGenerator(textToken, i)
        print generator.generate(500)
        print "-------------------------------------------------------"

main()
