'''
Chris Pellerito
CMPT 440 Final Project
This prgram is a version of the grep utility that takes
a regular expression and text file as input and returns
all full lines that match the regular expression.
'''
import sys


# create class for states
class state:
    def __init__(self, state):
        self.state = state
        self.tran = []
        self.accepts = False

    # create method to add tranistion to states
    def add_tran(self, in_state, to_state, value):
        self.tran.append([in_state, to_state, value])

    # create method to make a state accepting
    def set_accepts(self):
        self.accepts = True

    # create method to print states and if they accept or reject
    def print_states(self):
        if self.accepts:
            print("state: " + str(self.state) + " accepts")
        else:
            print("state: " + str(self.state) + " rejects")

    # create method to print the transitions
    def print_tran(self):
        if len(self.tran) > 0:
            for i in range(len(self.tran)):
                print("In state: " + self.tran[i][0])
                print("To state: " + self.tran[i][1])
                print("Value: " + self.tran[i][2])


def main():
    # open the inpuut file from stdin as input_file
    with open(sys.argv[2], 'r') as input_file:
        # reads lines from input file removes the \n and adds to list
        input_list = [line.rstrip() for line in input_file]

    # add reg expression from input to variable
    reg_exp = sys.argv[1]

    # convert the input from a list to a string to find the alphabet
    input_alpha = ''.join(input_list).lower()

    alphabet = ""  # initialize alphabet variable
    # checks if charcter from input is in alphabet, if not add to alpahbet
    for i in range(len(input_alpha)):
        if input_alpha[i] not in alphabet:
            alphabet += input_alpha[i]

    operators = "()+*"
    states = []  # empty list to hold the States objects
    previous = ""
    eps = "~e"  # create variable for value epsilon

    # check to make sure the regular expression is valid
    for check in reg_exp:
        # if check is not in the alphabet and not in operators
        # regular expression isn't valid
        if check not in alphabet and check not in operators:
            return "invalid regular expression"

    states.append(state("q0"))  # initialize start state
    # loop through the regular expression
    for i in range(len(reg_exp)):
        # if previous is +, set previous = to next value of reg expression
        # and continue to avoid infinite loop of previuos being +
        if previous == '+':
            previous = reg_exp[i]
            continue

        # if reg exp is ( create variable to keep track of where it is
        if reg_exp[i] == '(':
            para = i
            continue

        # if reg exp is ) set previous = to it and continue
        if reg_exp[i] == ')':
            previous = reg_exp[i]
            continue

        # if reg exp in alphabet create a state and transition
        if reg_exp[i] in alphabet:
            # create state object starting with q and ending with length of
            # states list - 1 to increment the states names correctly
            states.append(state("q" + str(len(states))))
            # add a transition to new state that has in state value of pervious
            # state and to state value of current state
            states[len(states) - 1].add_tran(states[len(states) - 2].state, states[len(states) - 1].state, reg_exp[i])
            previous = reg_exp[i]

        # if reg exp = + add same transition just created but change the value
        # to the next char in the reg exp and set previous = to + to avoid
        # creating new state next time through the loop
        elif reg_exp[i] == '+':
            states[len(states) - 1].add_tran(states[len(states) - 2].state, states[len(states) - 1].state, reg_exp[i + 1])
            previous = '+'

        # if reg exp = * and the last char in reg exp was a )
        # create epsilon transitions from where the parans started to where
        # they ended. If the first state in the parans is the starting state
        # and the last state in the parans last state, set the first state
        # to accepts
        elif reg_exp[i] == '*':
            if previous == ')':
                states[para].add_tran(states[para].state, states[len(states) - 1].state, eps)
                states[len(states) - 1].add_tran(states[len(states) - 1].state, states[para].state, eps)
                if states[para].state == "q0" and i == len(reg_exp) - 1:
                    states[0].set_accepts()

            # if previous isn't ) add transition from current state to curerent state
            else:
                states[len(states) - 1].add_tran(states[len(states) - 1].state, states[len(states) - 1].state, reg_exp[i - 1])
                previous = '*'

        # if i is the length of reg exp set last state to accepts
        if i == len(reg_exp) - 1:
            states[len(states) - 1].set_accepts()


main()
