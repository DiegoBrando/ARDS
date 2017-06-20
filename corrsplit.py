#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 00:20:10 2017

@author: ILabA2
"""

# code for splitting data and creating text files

#base directories
base="/NLPShare/ARDS/"
notetypes=base+"note_type.txt"
Cirr=base+"ARDS_Cirrhosis.csv"
CirrNotes=base+"cirrhosis_notes_09282016.txt"
ARDSPos=base+"/parsed/all/yes"
ARDSNeg=base+"/parsed/all/no"
import string
import os.path
import re


# Checks for ARDS results
def yorn(decision):
    dec=-1
    decision.upper()
    if decision=="YES":
        dec=1
    else:
        if decision=="NO":
            dec=0
    return dec


# function to check if the note_type matches the shorlisted types
def notet(note): 
    dec=0
    with open(notetypes,'r') as input_file:
        for line in input_file:
            cho1 = re.compile('\w+').findall(line) 
            cho2 = re.compile('\w+').findall(note) 
            if cho2 == cho1:
                dec=1
                
    return y



#creates copy of radiology notes
def mrns(dirc,mrn, rad): 
    copy_notes = ''.join(c for c in rad if c in string.printable)
    if dirc==1:
        file_name = os.path.join(ARDSPos,mrn+".txt")  # names file
    else:
        file_name = os.path.join(ARDSNeg,mrn+".txt") 
    out_file = open(file_name, 'a')  
    out_file.write(copy_notes + '\n') # creates copy of notes
    out_file.close()




# Returns Ards daignosis
def ards_result(mrn):
    result=0
    for line in open(Cirr,'r'):
        elements = line.split(',')
        mr1=str(elements[2]) 
        mr2=str(mrn) 
        if mr1 == mr2:
                result = elements[3].split('\n')               
    return result







c = 0
y = 0
n = 0
for line in open(CirrNotes,'r',encoding='utf-8', errors='ignore'):
    elements = line.split('||')
    c=c+1
    note = notet(elements[7])
    try:
       ards = int(elements[0])
    except ValueError:
       ards = None 
    ard=ards_result(ards)
    if (ard==1 and note==1): #Checks to see if ARDS is POSitive 
        y=y+1
        print("Positive Match Found", "## - ",y, "Mrn", ards)
        mrns(1,elements[0],elements[8])
    if (ard==0 and note==1): #Checks to see if ARDS is NEGitive
        n=n+1
        print("Negative match Found", "## - ",n, "Mrn", ards)
        mrns(0,elements[0],elements[8])
