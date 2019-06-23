'''
CARLOS EGUILUZ ROSAS
CYPHER PROGRAM v.1.0
UPDATED: 03-11-17
'''
from library_cypher import *

#####################
###CAESAR'S CIPHER###
#####################

def search_common(message):
    count = 0
    for i in range(len(message)):
        if message[i:i+2] in digramsList:
            count = count + 1
        if message[i:i+3] in trigramsList:
            count = count + 1
    return count

def fixShift(number):
    while number>26 or number<0 or isinstance(number,float):
        if isinstance(number,float):
            print "INVALID SHIFT: NUMBER MUST BE A WHOLE NUMBER"
            number = input('Enter a different shift number: ')
        else:
            number = number%26
    return number
            
def caesar(text,shiftNumber):
    beta = "abcdefghijklmnopqrstuvwxyz"
    alpha = shift_list("abcdefghijklmnopqrstuvwxyz",26-shiftNumber)
    message = ""
    for char in text:
        if char.isdigit() or (char in punc) or (char == " "):
            message += char
        else:
            message += alpha[beta.index(char)]
    return message

def bruteForce(message):
    print "List of Possibilities"
    
    possibleList = []
    frequency = []
    for i in range(26):#Presentation
        if i < 9:
            print ' '+str(i+1)+'. '+str(caesar(message,i))
        else:
            print str(i+1)+'. '+str(caesar(message,i))

        frequency.append(search_common(caesar(message,i)))
        possibleList.append(caesar(message,i))

    print 
    print "Possible Answer(s)"
    for j in range(len(frequency)):
        if frequency[j] == max(frequency):
            print possibleList[j]


#####################
###VIGENERE CIPHER###
#####################

def converter(given): #MAY NOT BE NECESSARY BUT LET US SEE...
    if isinstance(given,int):
        return value_letter[given]
    elif isinstance(given,str):
        return letter_value[given]

def extendKey(key,message):
    div = divmod(len(message),len(key))
    return key*div[0] + key[0:div[1]]
    
def vigenere(message,key,task): #works w/ no whitespaces => don't need # and punc case 
    secret = ""
    key = extendKey(key,message)
    for i in range(len(message)):
        a = "abcdefghijklmnopqrstuvwxyz".index(message[i])
        b = "abcdefghijklmnopqrstuvwxyz".index(key[i])
        if task == "encode":
            secret += tabula[a][b]
        else:
            secret += tabula[a][(26-b)%26]
    return secret
