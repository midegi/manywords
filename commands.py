# Michele De Giorgi
# Final Project Linguistica Computazionale 2020/2021
# commands.py 

# Importing all the necessary modules
import nltk
import re

# This function reads every line of the settings file and it returns a
# list for every lines. The settings file contains information about
# some commands useful to the program. For example, the language or
# the markov model set by the user.

def readsetting():
    with open("settings.txt", 'r') as settings:
        data = settings.read()

    # It takes in input all the lines in the file
    lines = re.split('\n', data)
    
    # It creates a list of strings. For example line1[0] = "language"
    # and line1[1] = "tokenizers/punkt/english.pickle"
    line1 = re.split(':\s', lines[0])
    line2 = re.split(':\s', lines[1])
    return line1, line2


# This function sets the language inserted in the terminal by the user.
def setlanguage(l):
    languages = {"eng" : "tokenizers/punkt/english.pickle",
                 "it" : "tokenizers/punkt/italian.pickle" 
    }

    choice = languages.get(l)
    
    # It calls the function readsetting() that returns the data in the
    # settings.txt file
    language, markov = readsetting()
    language[1] = choice
    data = [language, markov]

    # It writes in settings.txt the path of the correct .pickle file
    # based on the user choiche
    with open("settings.txt", 'w') as settings:
        settings.writelines('\n'.join('{}{} {}'.format(line[0],':',line[1]) for line in data))


# This function checks which language is currently set
def checklanguage():
    
    languages = {"tokenizers/punkt/english.pickle": "english",
                 "tokenizers/punkt/italian.pickle" : "italian" 
    }
    
    language, markov = readsetting()
    l = languages.get(language[1])
    print("The language currently set is",l) 

    

# This function writes the order of the markov, chain inserted in the
# terminal by the user, into the file settings.txt

def setmarkov(order):
    language, markov = readsetting()
    markov[1] = order
    data = [language, markov]
    
    with open("settings.txt", 'w') as settings:
        settings.writelines('\n'.join('{}{} {}'.format(line[0],':',line[1]) for line in data))

        

# This function checks which is the current order of the markov chain
# in the file settings.txt

def checkmarkov():
    language, markov = readsetting()
    order = int(markov[1])
    if order == 0:
        print("The model set is a markov model of zero order.")
    elif order == 1:
        print("The model set is a markov model of the first order.")

        

# This function checks the length of the *args argument passed to most
# of the functions in this file

def checkargs(data):
    
    f1 = data[0]
    
    # If args = 3 then there are a second corpus and a task 
    if len(data) == 3:
        f2 = data[1]
        task = data[2]
        if not task:
            task = None
        return f1, f2, task
    
    # If args = 2 then there is a task but there isn't a second corpus.
    # We set f2 to None.
    elif len(data) == 2:
        task = data[1]
        f2 = None
        if not task:
            task = None
        return f1, f2, task
    
    # If args = 1 then there isn't a task and there isn't a second
    # corpus. We create a taskpack object with all the arguments = None
    else:
        task = taskpack(None, None, None)
        f2 = None
        return f1, f2, task

    
# This function creates a list of two elements. It is needed to pass
# the list with the results to the printing functions, when the
# commands work with two corpora.

def condenser(d1, d2):
    data = []
    data.append(d1)
    data.append(d2)
    return data


# Declaration of the taskpack class with has three attributes: a name,
# which is equal to the name of the task, a value, which is equal to
# the value inserted in the terminal by the user and data, which is
# equal to the result of the commands executed by the user

class taskpack(object):
    def __init__(self, task, value, data):
        self.name = task
        self.value = value
        self.data = data

        
        
# This functions takes in input a filename and it makes the file ready
# for the computation analysis

def setup(filename):
    with open(filename, mode="r", encoding="utf-8") as f:
        raw = f.read()
        
    # It reads the settings.txt file
    language, markov = readsetting()
    
    # It creates the sent_tokenizer based on the input on the
    # language set
    sent_tokenizer = nltk.data.load(language[1])

    # It calls the condenser function
    data = condenser(raw, sent_tokenizer)
    return data



# This is the function called by the command "sentences". It  performs
# the sentence splitting by taking in input the first corpus, the
# second corpus and the task object. It also solve the various tasks

def tokenize_sentences(*args):

    # It calls the checkargs function to check how many arguments
    # are in the *args
    
    f1, f2, task = checkargs(args)

    # It checks if the user inserted the second corpus
    if f2:
        
        # It calls the setup function 2 times by passing the 2 different
        # files
        
        c1data = setup(f1)
        c2data = setup(f2)
        sent_tokenizer = c1data[1]
        raw1 = c1data[0]
        raw2 = c2data[0]
        c1_sentences = sent_tokenizer.tokenize(raw1)
        c2_sentences = sent_tokenizer.tokenize(raw2)

        # If there isn't a task the function returns only the result
        # of the main function. In this case, it returns only the
        # list of sentences of the 2 corpora 
        if task.name is None:
            data = condenser(c1_sentences, c2_sentences)
            return data

        else:
            
            # It checks which task was inserted by the user
            
            # It returns the number of senteces in the corpus
            if task.name == "corpuslength":
                C1L = Clength(c1_sentences)
                C2L = Clength(c2_sentences)
                data = condenser(C1L, C2L)
                
                # It creates a taskpack object by passing the result
                # Of the analysis on both of the two corpus
                
                result = taskpack(task.name, task.value, data)
                
                # It returns the taskpack object
                return result
            
            # It returns the average sentence length in terms of token
            elif task.name == "avgsentlen":
                c1_avglen = avglen(c1_sentences, "asl")
                c2_avglen = avglen(c2_sentences, "asl")
                data = condenser(c1_avglen, c2_avglen)
                result = taskpack(task.name, task.value, data)
                return result

    else:
        
        # It there isn't a second corpus it executes the same code but
        # just on one corpus
        
        data = setup(f1)
        raw = data[0]
        sent_tokenizer = data[1]
        sentences = sent_tokenizer.tokenize(raw)
        
        if task.name is None:
            return sentences

        else:
            if task.name == "corpuslength":
                CL = Clength(sentences)
                result = taskpack(task.name, task.value, CL)
                return result
            
            elif task.name == "avgsentlen":
                avg = avglen(sentences, "asl")
                result = taskpack(task.name, task.value, avg)
                return result


            
# This is the function called by the command "tokenize". It tokenizes
# all the corpus and it's structured in the same way of
# tokenize_sentences
def tokens(*args):
    
    f1, f2, task = checkargs(args)
    
    if f2:
        C1 = []
        sentences = tokenize_sentences(f1)
        for s in sentences:
            t = nltk.word_tokenize(s)
            C1 += t
        C2 = []
        sentences = tokenize_sentences(f2)
        for s in sentences:
            t = nltk.word_tokenize(s)
            C2 += t
            
        if task.name is None:
            data = condenser(C1, C2)
            return data
        
        else:
            # It returns the number of words in the corpus
            if task.name == "corpuslength":
               C1L = Clength(C1)
               C2L = Clength(C2)
               data = condenser(C1L, C2L)
               result = taskpack(task.name, task.value, data)
               return result
           
           # It returns the average length of all the sentences
           # in terms of tokens
            elif task.name == "avgtoklen":
               c1_avglen = avglen(C1, "atl")
               c2_avglen = avglen(C2, "atl")
               data = condenser(c1_avglen, c2_avglen)
               result = taskpack(task.name, task.value, data)
               return result

           # It returns the first n tokens of a corpus
            elif task.name == "ntoken":
                C1n = FNtokens(C1, task.value)
                C2n = FNtokens(C2, task.value)
                data = condenser(C1n, C2n)
                result = taskpack(task.name, task.value, data)
                return result      

    else:
        C1 = []
        sentences = tokenize_sentences(f1)
        for s in sentences:
            t = nltk.word_tokenize(s)
            C1 += t

        if task.name is None:
            return C1
        
        else:
            if task.name == "corpuslength":
                CL = Clength(C1)
                result = taskpack(task.name, task.value, CL)
                return result

            elif task.name == "avgtoklen":
                avg = avglen(C1, "atl")
                result = taskpack(task.name, task.value, avg)
                return result

            elif task.name == "ntoken":
                C1n = FNtokens(C1, task.value)
                result = taskpack(task.name, task.value, C1n)
                return result

            
            
# This function calculates all the n tokens in the corpus, based on the
# value inserted by the user 

def FNtokens(C, value):
    Cn = []
    for i in range(0, value):
        Cn.append(C[i])
    return Cn



# This function calcuates the average sentence length in terms of token
# and the average token length in terms of characthers

def avglen(C, t):
    CL = Clength(C)
    summed = 0
    if t == "asl":
        for s in C:
            TC = []
            t = nltk.word_tokenize(s)
            TC += t
            summed += len(TC)
        avg = summed / CL
        return avg
    
    if t == "atl":
        for t in C:
            summed += len(t)
        avg = summed / CL
        return avg
        

    
# This function calcuates the length of the corpus
def Clength(C):
    CL = len(C)
    return CL



# This is the function called by the command "vocabulary".
# It returns a list of all the word types of the corpus
def volcalc(*args):
    
    f1, f2, task = checkargs(args)
    
    if f2:
        C1 = tokens(f1)
        C2 = tokens(f2)
        V1 = []
        V2 = []
        V1 = list(set(C1))
        V2 = list(set(C2))

        if task.name is None:
            data = condenser(V1, V2)
            return data

        else:
            
            # It returns the total number of word types in the corpus
            if task.name == "voclength":
                V1L = Vlength(V1)
                V2L = Vlength(V2)
                data = condenser(V1L, V2L)
                result = taskpack(task.name, task.value, data)
                return result
                
            # It returns the type-token-ratio of the first n words
            if task.name == "typetokenratio":
                
                # It calls the function FNtokens to create the corpus of
                # the first n words. Value is n.
                
                TC1 = FNtokens(C1, task.value)

                # It creates the vocabulary of the corpus 
                TV1 = list(set(TC1))
                TCL1 = Clength(TC1)
                TVL1 = Vlength(TV1)

                # It passes the length of the vocabulary and the length
                # of the corpus
                ttr1 = TTR(TCL1, TVL1)

                TC2 = FNtokens(C2, task.value)
                TV2 = list(set(TC2))
                TCL2 = Clength(TC2)
                TVL2 = Vlength(TV2)
                ttr2 = TTR(TCL2, TVL2)
                
                data = condenser(ttr1, ttr2)
                result = taskpack(task.name, task.value, data)
                return result
       
    else:
        C1 = tokens(f1)
        V1 = []
        V1 = list(set(C1))

        if task.name is None:
            return V1

        else:
            if task.name == "voclength":
                VL1 = Vlength(V1)
                result = taskpack(task.name, task.value, VL1)
                return result

            if task.name == "typetokenratio":
                TC = FNtokens(C1, task.value)
                TV = list(set(TC))
                TCL = Clength(TC)
                TVL = Vlength(TV)
                ttr = TTR(TCL, TVL)
                result = taskpack(task.name, task.value, ttr)
                return result

            
            
# This function calculates the length of the vocabulary
def Vlength(V):
    VL = len(V) 
    return VL



# This function calculates the type-token-ratio
def TTR(CL, VL):
    TTR = VL / CL
    return TTR



# This function checks if a token is in a corpus
def checktoken(t, C):
    if t in C:
        return True
    else:
        return False

    
    
# This is the function called by the command "freq_distribution".
# It calculates the frequency of all the words in the corpus

def frequency_distribution(*args):
    
    f1, f2, task = checkargs(args)
    
    if f2:
        C1 = tokens(f1)
        C2 = tokens(f2)
        V1 = volcalc(f1)
        V2 = volcalc(f2)
        freqdist1 = nltk.FreqDist(C1)
        freqdist2 = nltk.FreqDist(C2)

        if task.name is None:
            data = condenser(freqdist1, freqdist2)
            return data
        
        else:
            
            # It returns the token with the maximum frequency
            if task.name == "fmax":
                
                # It passes the frequency distribution to FMax
                fmax1 = FMax(freqdist1)
                fmax2 = FMax(freqdist2)
                data = condenser(fmax1, fmax2)
                result = taskpack(task.name, task.value, data)
                return result

            # It returns the frequency of a token chosen by the user
            elif task.name == "token":
                
                # Token = the name of the token inserted by the user
                token = task.value

                # It passes the token and the corpus to checktoken
                if checktoken(token, C1):
                    # If the token is in the corpus, then
                    # dist1 = frequency of the token
                    dist1 = freqdist1[token]
                else:
                    dist1 = 0

                if checktoken(token, C2):
                    dist2 = freqdist2[token]
                else:
                    dist2 = 0

                data = condenser(dist1, dist2)
                result = taskpack(task.name, task.value, data)
                return result

            # It returns the frequency distribution of all the words
            # which have a frequency > of the value inserted by the user
            elif task.name == "freq":
                freq = task.value

                # It declares an empty list
                c1_freqdist = []
                
                # It creates an empty FreqDist object by using the
                # empty corpus
                fdist1 = nltk.FreqDist(c1_freqdist)
                
                # For every token in the frequency distribution,
                # it checks if the token frequency is > freq
                for t in freqdist1:
                    if freqdist1[t] >= freq:
                        # It adds the token and the frequency to the new
                        # empty object
                        fdist1[t] = freqdist1[t]

                c2_freqdist = []
                fdist2 = nltk.FreqDist(c2_freqdist)
                for t in freqdist2:
                    if freqdist2[t] >= freq:
                        fdist2[t] = freqdist2[t]

                data = condenser(fdist1, fdist2)
                result = taskpack(task.name, task.value, data)
                return result

            
            # It returns a list of all the tokens in a frequency class
            # chosen by the user
            elif task.name == "freqclass":
                # It directly passes to FClasses the file, its frequency
                # distribution and the task
                Vi1 = FClasses(f1, freqdist1, task)
                Vi2 = FClasses(f2, freqdist2, task)
                data = condenser(Vi1, Vi2)
                result = taskpack(task.name, task.value, data)
                return result


            # It returns a list of all the frequency classes in the
            # corpus
            elif task.name == "freqclasses":
                freqclasses1 = FClasses(f1, freqdist1, task)
                freqclasses2 = FClasses(f2, freqdist2, task)
                data = condenser(freqclasses1, freqclasses2)
                result = taskpack(task.name, task.value, data)
                return result

            
            # It returns the frequency distribution of all the words
            # which have a length > of the value inserted by the user
            elif task.name == "minlength":
                ml = task.value
                
                c1_freqdist = []
                fdist1 = nltk.FreqDist(c1_freqdist)
                for t in freqdist1:
                    if len(t) >= ml:
                        fdist1[t] = freqdist1[t]

                c2_freqdist = []
                fdist2 = nltk.FreqDist(c2_freqdist)
                for t in freqdist2:
                    if len(t) >= ml:
                        fdist2[t] = freqdist2[t]

                data = condenser(fdist1, fdist2)
                result = taskpack(task.name, task.value, data)
                return result

            
            # It returns the 2 frequency distributions that will be
            # plotted in a graph using Matprolib, in the print function
            elif task.name == "fgraph":
                freqdist = condenser(freqdist1, freqdist2)
                result = taskpack(task.name, task.value, freqdist)
                return result
                
    else:
        C = tokens(f1)
        V = volcalc(f1)
        freqdist = nltk.FreqDist(C)

        if task.name is None:
            return freqdist
        
        else:
            if task.name == "fmax":
                fmax = FMax(freqdist)
                result = taskpack(task.name, task.value, fmax)
                return result
    
            elif task.name == "token":
                token = task.value
                if checktoken(token, C):
                    dist = freqdist[token]
                else:
                    dist = 0

                result = taskpack(task.name, task.value, dist)
                return result
              
        
            elif task.name == "freq":
                freq = task.value
        
                c1_freqdist = []
                fdist1 = nltk.FreqDist(c1_freqdist)
                for t in freqdist:
                    if freqdist[t] >= freq:
                        fdist1[t] = freqdist[t]

                result = taskpack(task.name, task.value, fdist1)
                return result

            elif task.name == "freqclass":
                Vi = FClasses(f1, freqdist, task)
                result = taskpack(task.name, task.value, Vi)
                return result

            elif task.name == "freqclasses":
                freqclasses = FClasses(f1, freqdist, task)
                result = taskpack(task.name, task.value, freqclasses)
                return result
            
            elif task.name == "minlength":
                ml = task.value
                
                c1_freqdist = []
                fdist1 = nltk.FreqDist(c1_freqdist)
                for t in freqdist:
                    if len(t) >= ml:
                        fdist1[t] = freqdist[t]

                result = taskpack(task.name, task.value, fdist1)
                return result
    
            elif task.name == "fgraph":
                result = taskpack(task.name, task.value, freqdist)
                return result
                        

            
# This function identifies the token with the maximum frequency 
def FMax(freqdist):
    fmax = 0
    for t in freqdist:
        if freqdist[t] > fmax:
            fmax = freqdist[t]
            tmax = t
    return fmax, tmax



# This function calculates a group of types which have frequency equal
# to n. Also it calculates all the frequency classes of the corpus

def FClasses(f1, freqdist, task):
    
    C = tokens(f1)
    V = volcalc(f1)
    fmax, tmax = FMax(freqdist)
    freqclasses = []
    
    # It returns a list of all the frequency classes in the
    # corpus
    if task.name == "freqclasses":
        # It creates a list of empty lists, long as the frequency
        # of the token with the maximum frequency 
        for i in range(0, fmax+1, 1):
            freqclasses.append([])

        # For every token in the vocabulary, we count how many times
        # it appears in the corpus. Then we append the token to the
        # position of the list, which is equal to the frequency of the
        # token in the corpus.
        # For example, if the token "yeah" has a frequency of 5,
        # then we would append the token in freqclasses[5].
        for t in V:
            f = C.count(t)
            freqclasses[f].append(t)

        # It declares an empty list.
        Cpuppet = []
        
        # It creates an empty FreqDist object by using the
        # empty list 
        Vi = nltk.FreqDist(Cpuppet)
        
        for i in range(1, fmax+1, 1):
            # If the list is not empty, we calculate the length of the
            # frequency class. For example, Vi[5] would be equal to the
            # length of the frequency class where the tokens have
            # frequency = 5 
            if not freqclasses[i] == []:
                Vi[i] = len(freqclasses[i])

        return Vi

    
    # It returns a list of all the tokens in a frequency class
    # chosen by the user
    elif task.name == "freqclass":
        
        # For every token in the vocabulary, we count how many times
        # it appears in the corpus
        for t in V:
            f = C.count(t)
            # If its frequency = the frequency inserted by the user
            # then we append the token to the freqclasses list
            if f == task.value:
                freqclasses.append(t)

        return freqclasses
        

    
# This is the function called by the command "bigrams".
# It returns a list of all the bigrams in the corpus

def bigrams(*args):
    f1, f2, task = checkargs(args)
    
    if f2:
        C1 = tokens(f1)
        C2 = tokens(f2)
        B1 = list(nltk.bigrams(C1))
        B2 = list(nltk.bigrams(C2))
            
        if task.name is None:
            data = condenser(B1, B2)
            return data
        
        else:
            # It returns the frequency distribution of the bigrams
            # in the corpus
            if task.name == "bfreqdist":
                B1freqdist = nltk.FreqDist(B1) 
                B2freqdist = nltk.FreqDist(B2)
                freqdist = condenser(B1freqdist, B2freqdist)
                result = taskpack(task.name, task.value, freqdist)
                return result

    else:
        C = tokens(f1)
        B = list(nltk.bigrams(C))
       

        if task.name is None:
            return B
        
        else:
            if task.name == "bfreqdist":
                Bfreqdist = nltk.FreqDist(B)
                result = taskpack(task.name, task.value, Bfreqdist)
                return result



# This is the function called by the command "markov".
# It uses a language model based on Markov to calculate the probability
# of the sentences in the corpus

def markov(*args):
    
    f1, f2, task = checkargs(args)
    
    if f2:
        # It reads the settings.txt file in order to check what's the current
        # order 
        language, markov = readsetting()
        order = int(markov[1])

        
        if task.name is None:
            if order == 1:
                probdist1 = markov1(f1, task.name)
                probdist2 = markov1(f2, task.name)
            
                data = condenser(probdist1, probdist2)
                return data

    
        elif task.name == "setmarkov":
            task.value = int(task.value)
            # It passes the value chosen by the user (0 or 1) to
            # set the order of the markov chain
            setmarkov(task.value)
            checkmarkov()

        # It returns the smoothed probability calculated using the model
        elif task.name == "add1smoothing":
            if order == 1:
                probdist1 = markov1(f1, task.name)
                probdist2 = markov1(f2, task.name)
                data = condenser(probdist1, probdist2)
                return data

    else:
        language, markov = readsetting()
        order = int(markov[1])
        
        if task.name is None:
            if order == 1:
                probdist = markov1(f1, task.name)
                return probdist
        
        elif task.name == "setmarkov":
            task.value = int(task.value)
            setmarkov(task.value)
            checkmarkov()

    
        elif task.name == "add1smoothing":
            taskname = task.name
            if order == 1:
                probdist = markov1(f1, taskname)
            return probdist


        
# It calculates the probability of the sentences in the corpus using
# a markov chain of the first order
def markov1(f, taskname):
    
    S = tokenize_sentences(f)
    C = tokens(f)
    CL = Clength(C)
    V = volcalc(f)
    VL = Vlength(V)
    freqdist = frequency_distribution(f)
    
    # It creates a task object to calculate the frequency distribution of the
    # bigrams
    taskneed = taskpack("bfreqdist", None, None)
    Bfreqdist = bigrams(f, None, taskneed).data

    # It creates an empty list to store the probability
    probdist = []

    # It calculates the non-smoothed probability using a markov chain of the
    # first order
    if taskname is None:
        
        # It checks every sentences
        for s in S:
            
            # It calculates the token in the sentence
            tis = list(nltk.word_tokenize(s))
            
            # It calculates the bigrams in the sentence
            bis = list(nltk.bigrams(tis))
            
            # It calculates the probability of the first word using its relative
            # frequency
            P = freqdist[tis[0]] / CL
            
            # It calculates the conditional probability of every bigram in the
            # sentence
            for b in bis:
                # Frequency of the bigram
                bfreq = Bfreqdist[b]
                
                # Frequency of the first word of the bigram
                ft1 = freqdist[b[0]]
                
                # Conditional probability 
                cp = bfreq * 1.0 / ft1 * 1.0
                # It multiplies all the probability of the bigrams   
                P = P * cp
            couple = (s, P)
            probdist.append(couple)

        return probdist

    else:
        # It calculates the smoothed probability using a markov chain of the
        # first order
        for s in S:
            tis = list(nltk.word_tokenize(s))
            bis = list(nltk.bigrams(tis))
            P = (freqdist[tis[0]] + 1) / (CL + VL)
            for b in bis:
                bfreq = Bfreqdist[b] + 1
                ft1 = freqdist[b[0]] + VL
                cp = bfreq * 1.0 / ft1 * 1.0
                P = P * cp

            # It creates a tuple formed by the probability and the sentence
            couple = (s, P)

            # It appends the couple to the probability distribution
            probdist.append(couple)
                        
        return probdist
                


# This is the function called by the command "named_entities".
# It extracts all the named entities in the corpus
def NE_tagging(*args):
    
    f1, f2, task = checkargs(args)
    
    if f2:
        C1 = tokens(f1)
        C2 = tokens(f2)
        PoS1 = nltk.pos_tag(C1)
        PoS2 = nltk.pos_tag(C2)
        ne1 = nltk.ne_chunk(PoS1)
        ne2 = nltk.ne_chunk(PoS2)
        
        if task.name is None:
            data = condenser(ne1, ne2)
            return data

        # It returns the named entities in the iob format
        elif task.name == "iobformat":
            ne1 = nltk.chunk.tree2conllstr(ne1)
            ne2 = nltk.chunk.tree2conllstr(ne2)
            data = condenser(ne1, ne2)
            result = taskpack(task.name, task.value, data)
            return result

        # It returns the named entities found in the corpus
        elif task.name == "entfound":
            NElist1 = ext_entities(ne1)
            NElist2 = ext_entities(ne2)
            data = condenser(NElist1, NElist2)
            result = taskpack(task.name, task.value, data)
            return result

        else:
            data = condenser(ne1, ne2)
            result = taskpack(task.name, task.value, data)
            return result
            
    else:
        C1 = tokens(f1)
        PoS1 = nltk.pos_tag(C1)
        ne1 = nltk.ne_chunk(PoS1)
        
        if task.name is None:
            return ne1
        
        elif task.name == "iobformat":
            ne1 = nltk.chunk.tree2conllstr(ne1)
            result = taskpack(task.name, task.value, ne1)
            return result

        elif task.name == "entfound":
            NElist = ext_entities(ne1)
            result = taskpack(task.name, task.value, NElist)
            return result
                              
        else:
            result = taskpack(task.name, task.value, ne1)
            return result
    
                   

# This function returns the list of all the named entity in a corpus
def ext_entities(ne):

    NElist = []
    for node in ne:
        NE = ''
        if hasattr(node, 'label'):
            if node.label() in ["PERSON", "GPE", "ORGANIZATION"]:
                for NEtype in node.leaves():
                    NE = NE + ' ' + NEtype[0]
                    E = str(node.label())
                    couple = (E, NE)
                    NElist.append(couple)
                                
    NElist.sort(key = lambda x: x[0])
    return NElist
            
    
