# CMPT440FinalProject
Final project for CMPT 440

For this final prject I will be creating a version of the grep utility using python. This utility will be able to:
● Learn the alphabet from the input FILE.
● Convert the regular expression REGEX to a NFA.
● Convert the NFA to a DFA.
● Use DFA computation to test each line of the file for accept/reject.
● File lines are delimited by newline characters.
● Accepted lines should be printed to standard output.
● Output the NFA and/or DFA to the specified filenames in DOT language format.
It will also always match full lines and not substrings. It will act as if every regular expression has ^ at the begginning and $ at the end.

The syntax for this utility is:
python grepy [-d DFAFILE] [-n NFAFILE] regex file
