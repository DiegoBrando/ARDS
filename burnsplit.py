# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#file locations
base="/NLPShare/ARDS/"
notety=base+"note_type.txt"
ARDSburncsv=base+"ARDS_Burn.csv"
BurnNotes=base+"burn_notes_09282016.txt"
ARDSPos=base+"/parsed/all/yes"
ARDSNeg=base+"/parsed/all/no"



import re
import string
import os.path

# sees if the person is positive or negative for ARDS
def yorn(yn):
    choice=-1
    yn.upper()
    if yn=="YES":
        choice=1
    else:
        if yn=="NO":
            choice=0
    return choice


# Makes sure types match
def checktype(note): 
    cor=0
    with open(notety,'r') as input_file:
        for line in input_file:
            set1 = re.compile('\w+').findall(line)
            set2 = re.compile('\w+').findall(note)
            if set1 == set2:
                cor=1               
    return cor


# creates file with radiology notes

def mrns(direc,mrn, rad): 
    copy = ''.join(c for c in rad if c in string.printable)
    if direc==1:
        name = os.path.join(ARDSPos,mrn+".txt")  
    else:
        name = os.path.join(ARDSNeg,mrn+".txt") 
    # writes rad notes to file
    output = open(name, 'a')  
    output.write(copy + '\n') 
    output.close()
    

# Returns ARDS Diagnosis
def results(mrn):
    result=0
    for line in open(ARDSburncsv,'r'):
        elements = line.split(',')
        mrn1=str(elements[2]) # Gets MRN
        mrn2=str(mrn)    
        if mrn1 == mrn2:
                result = yorn(elements[3].split('\n')) #grabs ARDS label               
    return result



c = 0
y = 0
n = 0
for line in open(BurnNotes,'r',encoding='utf-8', errors='ignore'):
    elements = line.split('||')
    c=c+1
    note = checktype(elements[7])
    try:
       ards = int(elements[0])
    except ValueError:
       ards = None 
    ard=results(ards)
    if (ard==1 and note==1): #Rag notes POS
        y=y+1
        print("Positive Match", "## - ",y, "Mrn", ards)
        mrns(1,elements[0],elements[8])
    if (ard==0 and note==1): #Rad notes NEG
        n=n+1
        print("Negative Match", "## - ",n, "Mrn", ards)
        mrns(0,elements[0],elements[8])