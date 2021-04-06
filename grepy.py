#Chris Pellerito
#CMPT 440 Final Project
#This prgram is a version of the grep utility
import sys

with open(sys.argv[1], 'r') as inputFile:
    input = inputFile.read().replace("\n", '')      #read input from command line and replace new line characters with empty strings

alphabet = ""       #initialize alphabet variable
for i in range(len(input)):
    if input[i] not in alphabet:
        alphabet += input[i]        #check if charcter from input is in alphabet, if not add to alpahbet

