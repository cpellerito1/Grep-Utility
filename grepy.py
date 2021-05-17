'''
Chris Pellerito
CMPT 440 Final Project
This prgram is a version of the grep utility that takes
a regular expression and text file as input and returns
all full lines that match the regular expression.
'''
import copy
import argparse


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


def compute(accept_states, transitions, input_str):
    # compute on NFA
    # set current state to initial state
    current_state = "q0"
    # loop[ through the input string for each character]
    for t in input_str:
        fail = 0  # initialize fail check
        # loop through the list of transitions, if the current state =
        # to the in_state of a transition, check if the value of that
        # transition = to t. If it is set current state to to_state
        for trans in transitions:
            if trans[0] == current_state:
                if trans[2] == t:
                    current_state = trans[1]
            else:
                fail += 1
                # if you gop through the whole list of transitions and
                # none have the same in_state and value, return False
                if fail == len(transitions):
                    return False
    # if you go through the entire string and the current state
    # is in the list of accepting states return True, otherwise false
    if current_state in accept_states:
        return True

    else:
        return False


def main():
    # initialize parser for CLI arguments
    parser = argparse.ArgumentParser()
    # create optional paramater for NFA output file
    parser.add_argument("-n", help="File name of NFA output file", type=str)
    # create optional parameter for DFA output file
    parser.add_argument("-d", help="File name of DFA output file", type=str)
    # create parameter for reg exression
    parser.add_argument("regex")
    # create paramter for input file
    parser.add_argument("file")
    args = parser.parse_args()

    # open the inpuut file from stdin as input_file
    with open(args.file, 'r') as input_file:
        # reads lines from input file removes the \n and adds to list
        input_list = [line.rstrip() for line in input_file]

    # add reg expression from input to variable
    reg_exp = args.regex

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
    accept_states = []  # empty list to hold accepting states

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
                    accept_states.append(states[0].state)

            # if previous isn't ) add transition from current state to curerent state
            else:
                states[len(states) - 1].add_tran(states[len(states) - 1].state, states[len(states) - 1].state, reg_exp[i - 1])
                previous = '*'

        # if i is the length of reg exp set last state to accepts
        if i == len(reg_exp) - 1:
            states[len(states) - 1].set_accepts()
            accept_states.append(states[len(states) - 1].state)

    # NFA to DFA
    # deepcopy states to dfa_states so NFA stays unchanged and DFA
    # can be manipulated
    dfa_states = copy.deepcopy(states)
    # add another state to be the trap state
    dfa_states.append(state("q" + str(len(dfa_states))))
    # loop through list of objects to add/remove transitions
    for dfa in range(len(dfa_states)):
        alpha = ""
        if len(dfa_states[dfa].tran) > 0:
            # add all values that you transition on to a variable to check
            # if all charcters of the alphabet have a transition
            for p in dfa_states[dfa].tran:
                if p[2] in alphabet:
                    alpha += p[2]
                # if transition value is an epsilon remove transition
                if p[2] == eps:
                    dfa_states[dfa].tran.remove(p)

            # check if all characters of alphabet have a transition
            for m in alphabet:
                if m not in alpha:
                    dfa_states[dfa].add_tran(dfa_states[dfa - 1].state, "q" + str((len(dfa_states) - 1)), m)

    # compute on NFA
    # create list of accepting states
    for accept in dfa_states:
        if accept.accepts:
            accept_states.append(accept.state)

    # create list of all transitions for easy access
    transitions = []
    for index in states:
        if len(index.tran) == 1:
            transitions.append(index.tran[0])

        elif len(index.tran) > 1:
            for x in index.tran:
                transitions.append(x)

    # call compute function on the NFA
    for input_str in input_list:
        # if compute function returns True print the input
        if compute(accept_states, transitions, input_str):
            print(input_str)

    # output NFA
    # if optional parameter is not empty open file with name from CLI
    if args.n is not None:
        nfa_file = open(args.n, "w")
        for out in transitions:
            if out[1] in accept_states:
                nfa_file.write(out[0] + "->" + out[1] + "[label=" + out[2] + "] accepts" + "\n")
            else:
                nfa_file.write(out[0] + "->" + out[1] + "[label=" + out[2] + "]" + "\n")

    # output DFA
    # create list of all transitions
    dfa_transitions = []
    for dfa_index in dfa_states:
        if len(dfa_index.tran) == 1:
            dfa_transitions.append(dfa_index.tran[0])

        elif len(dfa_index.tran) > 1:
            for n in dfa_index.tran:
                dfa_transitions.append(n)

    # if optional paramter is not empty open file with name from CLI
    if args.d is not None:
        dfa_file = open(args.d, "w")
        for dfa_out in dfa_transitions:
            if dfa_out[1] in accept_states:
                dfa_file.write(dfa_out[0] + "->" + dfa_out[1] + "[label=" + dfa_out[2] + "] accepts" + "\n")
            else:
                dfa_file.write(dfa_out[0] + "->" + dfa_out[1] + "[label=" + dfa_out[2] + "]" + "\n")

main()
