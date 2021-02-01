# Michele De Giorgi
# Final Project Linguistica Computazionale 2020/2021
# manywords.py 

# Importing all the necessary modules
import argparse
from commands import *
from printers import *


# Declaration of the output class which has two attributes: a
# destination and a boolean value that verify if the user requested an
# output to an external file
class otf(object):
    def __init__(self, o, dest):
        self.o = o
        self.dest = dest

        
# Declaration of the task class which has two attributes: a name and
# the value entered by the user
class task(object):
    def __init__(self, task, value):
        self.name = task
        self.value = value

        
# This function checks if and which argument the user has inserted
# in the terminal
def checktask(args):
    tasks = ["ntoken", "corpuslength", "avgsentlen", "avgtoklen", "voclength", "typetokenratio", "token", "freq", "freqclass", "freqclasses", "fmax", "minlength", "fgraph", "bfreqdist", "setmarkov", "add1smoothing","iobformat", "nodeprint", "entfound"]
    name = None
    value = None
    
    for t in tasks:
        if t in args:
            name = t  
            value = getattr(args, t)

    # Creation of a task object
    todo = task(name, value)
    return todo


# This function checks if the user requested an output to an external
# file 
def checkoutput(o, args):
    if o:
        dest = args.output
    else:
        dest = None
    return dest


# This function calls other functions from the module printers.py
# in order to print the data. The function takes in input the command
# inserted by the user, the first file, the second file, which can be
# none, and the object otp, which also can be none

def printer(data, comm, f1, f2, tofile):
    
    # We use a dictionary that associates a command to a specific output
    # function
    printcomm = {"sentences" : print_lists,
                "tokenize" : print_lists,
                "vocabulary" : print_lists,
                "freq_distribution" : print_frequency,
                "bigrams" : print_bigrams,
                "markov" : print_probability,
                "named_entities" : print_NEtagging
    }

    # Passing to the output function the same data the function taken
    # in input 
    data = printcomm.get(comm)(data, f1, f2, tofile)
            


# The main function of the program
def main():
    
    # The dictionary associates a command to a specific function in
    # commands.py. 
    commands = {"sentences" : tokenize_sentences,
                "tokenize" : tokens,
                "vocabulary" : volcalc,
                "freq_distribution" : frequency_distribution,
                "bigrams" : bigrams,
                "markov" : markov,
                "named_entities" : NE_tagging
    }

    # Creation of a parser object using the argparse module.
    # We also add a subparser to the parser object in order to define a
    # command
    parser = argparse.ArgumentParser(description='Quantive analysis with nltk')
    subparsers = parser.add_subparsers(dest = "command")

    
    # Setlanguage command
    # Set the language in which the script operates
    setlanguage_parser = subparsers.add_parser('setlanguage', help='Set the desired language in which the program operates')
    setlanguage_parser.add_argument('l', action='store', default="eng", choices=["eng", "it"], help='Directory to list')

    
    # Checklanguage command
    # Check which language is currently set
    checklanguage_parser = subparsers.add_parser('checklanguage', help='It checks which language is currently set')

    
    # Sentences splitter command
    # It returns a list of all phrases in the corpus
    sentences_parser = subparsers.add_parser('sentences', help='It returns a list of all phrases in the corpus')
    # Creation of a mutually exclusive group that forces the user to
    # choose just one argument, aka just 1 task
    megroup = sentences_parser.add_mutually_exclusive_group()
    sentences_parser.add_argument('corpus', help='Specify the corpus to analyze')
    # Declaration of an argument to specify if there is a second corpus
    # to analyze
    sentences_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup.add_argument("-cl", "--corpuslength", action="store_true", default=argparse.SUPPRESS, help="Calculate the length of the corpus")
    megroup.add_argument("-asl", "--avgsentlen", action="store_true", default=argparse.SUPPRESS, help="Calculate the average tokens in the sentences")
    sentences_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="It directs the output to a filename of your choice")

    
    # Tokenize command
    # It returns a list of all the words in the corpus
    tokenize_parser = subparsers.add_parser("tokenize", help="It returns a list of all the words in the corpus")
    megroup = tokenize_parser.add_mutually_exclusive_group()
    tokenize_parser.add_argument("corpus", help="Specify the corpus to analyze")
    tokenize_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup.add_argument("-n", "--ntoken", type=int, default=argparse.SUPPRESS, help="Returns a list of the n words in the corpus")
    megroup.add_argument("-cl", "--corpuslength", action="store_true", default=argparse.SUPPRESS, help="Calculate the length of the corpus")
    megroup.add_argument("-atl", "--avgtoklen", action="store_true", default=argparse.SUPPRESS, help="Calculate the average tokens in the sentences")
    tokenize_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="It directs the output to a filename of your choice")

    
    # Vocabulary command
    # It returns a list of all the word types of the corpus
    vocabulary_parser = subparsers.add_parser("vocabulary", help="It returns a list of all the word types of the corpus")
    vocabulary_parser.add_argument("corpus", help="Specify the corpus to analyze")
    vocabulary_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup = vocabulary_parser.add_mutually_exclusive_group()
    megroup.add_argument("-vl", "--voclength", action="store_true", default=argparse.SUPPRESS, help="Calculate the length of the vocabulary")
    megroup.add_argument("-ttr", "--typetokenratio", type=int, default=argparse.SUPPRESS, help="Calculate the type-toke-ratio (vocabulary variation) of the first n tokens in the corpus.")
    vocabulary_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="Directs the output to a name of your choice")

   
    # Freq_distribution command
    # It calculates the frequency of all the words in the corpus
    freqdist_parser = subparsers.add_parser("freq_distribution", help="It calculates the frequency of all the words in the corpus")
    freqdist_parser.add_argument("corpus", help="Specify the corpus to analyze")
    freqdist_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup = freqdist_parser.add_mutually_exclusive_group()
    megroup.add_argument("-t", "--token", type=str, default=argparse.SUPPRESS, help="Specify the token whose frequency you want to know")
    megroup.add_argument("-f", "--freq", type=int, default=argparse.SUPPRESS, help="It specifies the minimum frequency which the words need to have in order to appear in the frequency distribution")
    megroup.add_argument("-fc", "--freqclass", type=int, default=argparse.SUPPRESS, help="It calculates a group of types which have frequency equal to n.")
    megroup.add_argument("-fcs", "--freqclasses", action="store_true", default=argparse.SUPPRESS, help="It calculates all the frequency classes of the corpus.")
    megroup.add_argument("-ml", "--minlength", type=int, default=argparse.SUPPRESS, help="It specifies the minimum length which the words need to have in order to appear in the frequency distribution")
    megroup.add_argument("-fg", "--fgraph", type=int, default=argparse.SUPPRESS, help="The function returns a graph which plots the n most frequent words. It requires Mathprolib with pyplot to work")
    megroup.add_argument("-fm", "--fmax", action="store_true", default=argparse.SUPPRESS, help="It finds the word with the max frequency")
    freqdist_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="It directs the output to a filename of your choice")

    
    # Bigrams command
    # It returns a list of all the bigrams in the corpus
    bigrams_parser = subparsers.add_parser("bigrams", help="It returns a list of all the bigrams in the corpus")
    megroup = bigrams_parser.add_mutually_exclusive_group()
    bigrams_parser.add_argument("corpus", help="Specify the corpus to analyze")
    bigrams_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup.add_argument("-fd", "--bfreqdist", action="store_true", default=argparse.SUPPRESS, help="Calculate the frequency of all the bigrams in the corpus")
    bigrams_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="It directs the output to a filename of your choice")

    
    # Markov Model command
    # It uses a language model based on Markov to calculate the probability of the sentences in the corpus
    markov_parser = subparsers.add_parser("markov", help="It uses a language model based on Markov to calculate the probability of the sentences in the corpus")
    megroup = markov_parser.add_mutually_exclusive_group()
    markov_parser.add_argument("corpus", help="Specify the corpus to analyze")
    markov_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup.add_argument('-add1','--add1smoothing',  action='store_true',  default=argparse.SUPPRESS,  help="It uses the add-one smoothing alghoritm to calculate the probability of the sentences")
    megroup.add_argument('-sm','--setmarkov',  action="store", choices=["0","1"],  default=argparse.SUPPRESS, help="It specifies the order of the markov chain that has to be used")
    markov_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="It directs the output to a filename of your choice")

    
    # Named Entity Tagging command
    # Command which extracts all the named entities in the corpus
    netagging_parser = subparsers.add_parser("named_entities", help="It extracts all the named entities in the corpus")
    megroup = netagging_parser.add_mutually_exclusive_group()
    netagging_parser.add_argument("corpus", help="Specify the corpus to analyze")
    netagging_parser.add_argument('-c2','--corpus2', default=argparse.SUPPRESS, help='Specify the second corpus to analyze')
    megroup.add_argument('-np','--nodeprint',  action='store_true',  default=argparse.SUPPRESS,  help="It prints all the nodes of the tree")
    megroup.add_argument('-iob','--iobformat',  action='store_true',  default=argparse.SUPPRESS,  help="It prints the result in the IOB format")
    megroup.add_argument('-ent','--entfound',  action='store_true',  default=argparse.SUPPRESS,  help="It prints all the entities found in the sentences")
    netagging_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="It directs the output to a filename of your choice")
  
 
    # The arguments are parsed with parse_args(). The parsed arguments
    # are present as object attributes.
    args = parser.parse_args()

    if args.command is None:
        print("Please, write manywords.py -h to list all the commands")
        
    # It checks if the command entered by the user is setlanguage
    elif args.command == "setlanguage":
        
        # It takes the value chosen by the user and pass to the
        # setlanguage function in commands.py
        setlanguage(args.l)
        
        # It calls the checklanguage function
        checklanguage()
        
    elif args.command == "checklanguage":
        checklanguage()
        
    else:
        # It takes the first corpus in input 
        filename = args.corpus
        
        # It checks if corpus is inserted by the user
        c2 = "corpus2" in args
        
        if c2:
            # It takes the second coprus in input
            filename2 = args.corpus2
            
            # It takes the command in input
            comm = args.command

            # Pass the args to the checktask function, which returns a
            # task object
            task = checktask(args)

            # It sends to the right function of commands.py the first
            # file, the second file and the task. The function called
            # returns the elaborated data that is ready to be printed
            data = commands.get(comm)(filename, filename2, task)

            # Check if the user wants the output to an external file
            o = "output" in args

            # It sets the destination of the output by calling the
            # checkoutput function 
            dest = checkoutput(o, args)

            tofile = otf(o, dest)

            printer(data, comm, filename, filename2, tofile)
            
        else:
            filename2 = None
            comm = args.command
            task = []
            task = checktask(args)
            data = commands.get(comm)(filename, filename2, task)
            
            o = "output" in args
            dest = checkoutput(o, args)
            tofile = otf(o, dest)
           
            printer(data, comm, filename, filename2, tofile)
        

    
   
main()

