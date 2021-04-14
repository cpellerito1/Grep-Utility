'''
Chris Pellerito
CMPT 440 Final Project
This prgram is a version of the grep utility that takes
a regular expression and text file as input and returns
all full lines that match the regular expression.
'''
import sys


def main():
    # store the regular expression from stdin as string
    reg_expression = sys.argv[1]

    # open the inpuut file from stdin as input_file
    with open(sys.argv[2], 'r') as input_file:
        # reads lines from input file removes the \n and adds to list
        input_list = [line.rstrip() for line in input_file]

    # convert the input from a list to a string to find the alphabet
    input_str = ''.join(input_list)

    alphabet = ""  # initialize alphabet variable
    # checks if charcter from input is in alphabet, if not add to alpahbet
    for i in range(len(input_str)):
        if input_str[i] not in alphabet:
            alphabet += input_str[i]

    operators = "()+*"
    accepts = []  # ionitialize list of accepting strings
    # checks if there are any operators in the reg expression
    # if not, adds any strings that match reg expression to accepting string
    if operators not in reg_expression:
        for index in input_list:
            if index == reg_expression:
                accepts.append(index)

    for x in accepts:
        print(x + "\n")


main()
