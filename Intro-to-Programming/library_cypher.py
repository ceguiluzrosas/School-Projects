'''
CARLOS EGUILUZ ROSAS
CYPHER PROGRAM v.1.0
UPDATED: 03-11-17
'''

######################
###LIBRARY FOR CODE###
######################


#List of Common 2 Letters
digramsList = ['th', 'he', 'in', 'er', 'an', 're', 'ed', 'on',
               'es', 'st', 'en', 'at', 'to', 'nt', 'ha', 'nd',
               'ou', 'ea', 'ng', 'as', 'or', 'ti', 'is', 'et',
               'it', 'ar', 'te', 'se', 'hi', 'of']

#List of Common 3 Letters
trigramsList = ['the', 'ing', 'and', 'her', 'ere', 'ent', 'tha',
                'nth', 'was', 'eth', 'for', 'dth']

#(LETTER,VALUE) and (VALUE,LETTER)
letter_value = {}
value_letter = {}
def alphabet_value():
    alpha = " abcdefghijklmnopqrstuvwxyz"
    value = 0
    for char in alpha:
        letter_value[char] = value
        value_letter[value] = char
        value += 1
alphabet_value()

#Punctuation Marks
punc = ["!",":",",",".","'","-","(",")","?",";","[","]"]

#Vigenere Table
tabula = []
def shift_list(lst,shift):
    return lst[-shift::]+lst[:-shift]

def tabula_recta():
    for i in range(26):
        tabula.append(shift_list('abcdefghijklmnopqrstuvwxyz',26-i))
tabula_recta()

        

