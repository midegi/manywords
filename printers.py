# Michele De Giorgi
# Final Project Linguistica Computazionale 2020/2021
# printers.py

# Importing all the necessary modules
import matplotlib.pyplot as plt
import re
from commands import taskpack


# This function takes in input the \\task, the first corpus, the second
# corpus and the tofile object. It checks which task the user requested
# and what function to use to print the result

def checktask(task, f1, f2, tofile):
    
    # Data = the result of the analysis done in commands.py
    data = task.data
    
    # Value = the value inserted by the user in the terminal
    value = task.value
    if task.name == "ntoken":
        print_lists(data, f1, f2, tofile)
    elif task.name == "corpuslength":
        print_Clength(data, f1, f2, tofile)
    elif task.name == "avgsentlen":
        print_avgsentlen(data, f1, f2, tofile)
    elif task.name == "avgtoklen":
        print_avgtoklen(data, f1, f2, tofile)
    elif task.name == "voclength":
        print_Vlength(data, f1, f2, tofile)
    elif task.name == "typetokenratio":
        print_TTR(data, f1, f2, tofile)
    elif task.name == "fmax":
        print_FMax(data, value, f1, f2, tofile)
    elif task.name == "token":
        print_FToken(data, value, f1, f2, tofile)
    elif task.name == "freq":
        print_frequency(data, f1, f2, tofile)
    elif task.name == "freqclass":
        print_freqclass(data, value, f1, f2, tofile)
    elif task.name == "freqclasses":
        print_freqclass(data, value, f1, f2, tofile)
    elif task.name == "minlength":
        print_frequency(data, f1, f2, tofile)
    elif task.name == "fgraph":
        print_FGraph(data, value, f1, f2, tofile)
    elif task.name == "bfreqdist":
        print_Bfrequency(data, value, f1, f2, tofile)
    elif task.name == "iobformat":
        print_NEtagging(data, f1, f2, tofile)
    elif task.name == "entfound":
        print_entfound(data, f1, f2, tofile)
    elif task.name == "nodeprint":
        print_nodeprint(data, f1, f2, tofile)

        

# This function writes m to an external destination specified by the
# user

def output(dest, m):
    with open(dest, 'w') as output_file:
        output_file.writelines(m)


# This function creates a doublepath based on the destination specified
# by the user. For example, if dest = "try.txt", we would have
# "try_<namefile1>.txt and try_<namefile2>.txt

def doublepath(f1, f2, dest):
    
    # It separates the name of the destination file from its extension
    filename = re.split('\.', dest)
    
    # It adds the string "_<namefile1>" to the first destination
    tofile1 = filename[0] + "_" + f1
    tofile2 = filename[0] + "_" + f2
    return tofile1, tofile2


# This is the function which prints the result of the commands
# "sentences", "tokenize" and "vocabulary". The function takes in input
# the data, which can be a list or a taskpack object, the first corpus,
# the second corpus and the tofile object

def print_lists(data, f1, f2, tofile):

    # It checks if the second corpus is None
    if f2 is None:
        
        # It checks if data is a list 
        if type(data) == list:
            # If tofile.o is true, then it prints the result to an
            # external file. 
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    # It prints an element per line 
                    output_file.writelines("%s\n" % i for i in data)
            else:
                for t in data:
                    print(t)
        else:
            # If data is not a list, then it's a taskpack object. So it
            # calls the checktask function by passing the same arguments
            # of the print_lists functionts
            checktask(data, f1, f2, tofile)
    else:
        
        # In this case the second corpus is not None 
        if type(data) == list:
            
            # It checks if it's a list. If the second corpus is not none
            # then we have the result of the first corpus and the result
            # of the second.

            # Result of the first corpus
            c1 = data[0]

            # Result of the second corpus
            c2 = data[1]
            if tofile.o:
                
                # It calls the doublepath function to create the
                # double path
                
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                
                with open(tofile1, 'w') as output_file:
                    output_file.writelines("%s\n" % t for t in c1)
                    
                with open(tofile2, 'w') as output_file:
                    output_file.writelines("%s\n" % t for t in c2)
            else:
                
                print(f1)
                for t in c1:
                    print(t)
                    
                # It prints 3 empty spaces between the results
                for s in range(3):
                    print()

                print(f2)
                for t in c2:
                    print(t)
                   
        else:
            checktask(data, f1, f2, tofile)

            
# This function prints the result of the avgsentlent task
def print_avgsentlen(avg, f1, f2, tofile):
    
    if f2 is None:
        
        if tofile.o:
            m = "The file " + str(f1) + " has an average of " + str(avg) + " words per sentence."

            # It passes the message and the destination to the output
            # function
            output(tofile.dest, m)
            
        else:
            print("The file",f1, "has an average of", avg, "words per sentence.")
            
    else:
        avg1 = avg[0]
        avg2 = avg[1]
        
        if tofile.o:
            m = "The file " + str(f1) + " has an average of " + str(avg1) + " words per sentence."
            m += "\n" + "The file " + str(f2) + " has an average of " + str(avg2) + " words per sentence."
            
            output(tofile.dest, m)
            
        else:
            print("The file",f1, "has an average of", avg1, "words per sentence.")
            print("The file",f2, "has an average of", avg2, "words per sentence.")


            
# This function prints the result of the avgtoklen task
def print_avgtoklen(avg, f1, f2, tofile):
    
    if f2 is None:
        if tofile.o:
            # It creates the str that has to be printed in the external
            # file.
            m = "The file " + str(f1) + " has an average of " + str(avg) + " characters per word."
            
            output(tofile.dest, m)
            
        else:
            print("The file",f1, "has an average of", avg, "characters per word.")
            
    else:
        avg1 = avg[0]
        avg2 = avg[1]
        
        if tofile.o:
            m = "The file " + str(f1) + " has an average of " + str(avg1) + " characters per word."
            m += "\n" + "The file " + str(f2) + " has an average of " + str(avg2) + " characters per word.."
            output(tofile.dest, m)
            
        else:
            print("The file",f1, "has an average of", avg1, "characters per word.")
            print("The file",f2, "has an average of", avg2, "characters per word.")
        

                
# This function prints the result of the corpuslength task   
def print_Clength(CL, f1, f2, tofile):
    
    if f2 is None:
        if tofile.o:
            m = "The file " + str(f1) + " is long " + str(CL) + " tokens."
            output(tofile.dest, m)
            
        else:
                print("The file", f1, "is long", CL, "tokens.")
    else:
        
        C1L = CL[0]
        C2L = CL[1]
        if tofile.o:
            
            m = "The file " + str(f1) + " is long " + str(C1L) + " tokens."
            m = m + "\n" + "The file " + str(f2) + " is long " + str(C2L) + " tokens."
            if C1L > C2L:
                m = m + "\n" + "The file " + str(f1) + " is longer than " + str(f2) + " by ", str(C1L-C2L) + " tokens."

            elif C2L > C1L:
                m = m + "\n" + "The file " + str(f2) + " is longer than " + str(f1) + " by ", str(C2L-C1L) + " tokens."

            else:
                m = m + "\n" + "The files " + str(f1) + " and " + str(f2) + " have the same length."
                
            output(tofile.dest, m)
            
        else:
            print("The file", f1, "is long", C1L, "tokens.")
            print("The file", f2, "is long", C2L, "tokens.")
            if C1L > C2L:
                print("The file", f1, "is longer than", f2, "by", C1L-C2L, "tokens.")
            elif C2L > C1L:
                print("The file", f2, "is longer than", f1, "by", C2L-C1L, "tokens.")
            else:
                print("The files", f1, "and", f2, "have the same length.")


                

# This function prints the result of the voclength task   
def print_Vlength(V, f1, f2, tofile):
    
    if f2 is None:
        if tofile.o:
            m = "The file " + str(f1) + " has " + str(V) + " words type."
            output(tofile.dest, m)
            
        else:
                print("The file", f1, "has", V, "words type.")
    else:
        V1L = V[0]
        V2L = V[1]
        if tofile.o:
            
            m = "The file " + str(f1) + " has " + str(V1L) + " words type."
            m = m + "\n" + "The file " + str(f2) + " has " + str(V2L) + " words type."
            if V1L > V2L:
                m = m + "\n" + "The file " + str(f1) + " has " + str(V1L-V2L) + " more words type than " + str(f2)
            elif V2L > V1L:
                m = m + "\n" + "The file " + str(f2) + " has " + str(V2L-V1L) + " more words type than " + str(f1)
            else:
                m = m + "\n" + "The files " + str(f1) + " and " + str(f2) + " have the same word types." 
  
            output(tofile.dest, m)
            
        else:
            print("The file", f1, "has", V1L, "words type.")
            print("The file", f2, "has", V2L, "words type")
            if V1L > V2L:
                print("The file", f1, "has", V1L-V2L, "more words type than", f2)
            elif V2L > V1L:
                print("The file", f2, "has", V2L-V1L, "more words type than", f1)
            else:
                print("The files", f1, "and", f2, "have the same word types.")



                
# This function prints the result of the ttr task. The result can't be
# exported to an external file

def print_TTR(TTR, f1, f2, tofile):
    
    if f2 is None:
        print("The type-token-ratio of", f1, "is", TTR)
    else:
        TTR1 = TTR[0]
        TTR2 = TTR[1]
        print("The type-token-ratio of", f1, "is", TTR1)
        print("The type-token-ratio of", f2, "is", TTR2)



# This is the function which prints the result of the commands
# "freq_distribution". The function takes in input
# the data, which can be a freqdist object, a list or a taskpack object,
# the first corpus, the second corpus and the tofile object

def print_frequency(data, f1, f2, tofile):
    
    if f2 is None:
        
        # It checks if data is a taskpack object
        if isinstance(data, taskpack) == False:
            freqdist = data
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {}'.format(freqdist[t],'\t',t) for t in freqdist))
            else:
                print("Freq \t token")
                for t in freqdist:
                    print(freqdist[t], "\t", t)
        else:
            checktask(data, f1, f2, tofile)
                              
    else:
        if type(data) == list:
            freqdist1 = data[0]
            freqdist2 = data[1]
            if tofile.o:
            
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {}'.format(freqdist1[t],'\t',t) for t in freqdist1))
                with open(tofile2, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {}'.format(freqdist2[t],'\t',t) for t in freqdist2))
            else:
                print(f1)
                print("Freq \t token")
                for t in freqdist1:
                    print(freqdist1[t], "\t", t)
                for s in range(3):
                    print()

                print(f2)
                for t in freqdist2:
                    print(freqdist2[t], "\t", t)
        
         
        else:
            checktask(data, f1, f2, tofile)



            
# This function prints the result of the FMax task. The result can't be
# exported to an external file

def print_FMax(fmax, value, f1, f2, tofile):
    
    if f2 is None:
        print("The most frequent token in", f1, "is", fmax[1], "which appears", fmax[0], "times in the corpus.")
    else:
        fmax1 = fmax[0]
        fmax2 = fmax[1]
        print("The most frequent token in", f1, "is", fmax1[1], "which appears", fmax1[0], "times in the corpus.")
        print("The most frequent token in", f2, "is", fmax2[1], "which appears", fmax2[0], "times in the corpus.")


        

# This function prints the result of the FToken task. The result can't 
# be exported to an external file

def print_FToken(ftoken, value, f1, f2, tofile):
    
    if f2 is None:
        print("The token", value, "appears", ftoken, "in", f1)
    else:
        ftoken1 = ftoken[0]
        ftoken2 = ftoken[1]
        if ftoken1 == 0:
            print("The token", value, "doesn't appear in", f1)
        else:
            print("The token", value, "appears", ftoken1, "in", f1)

        if ftoken2 == 0:
            print("The token", value, "doesn't appear in", f2)
        else:
            print("The token", value, "appears", ftoken2, "in", f2)

            

# This function prints the result of the freqclass and freqclasses task

def print_freqclass(data, value, f1, f2, tofile):

    if f2 is None:
        
        # It prints the frequency class chosen by the user in 1 corpus 
        if type(data) == list:
             if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines("%s\n" % i for i in data)
             else:
                print("Class", value)
                for t in data:
                    print(t)
        else:
            # It prints the frequency classes of 1 corpus
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {}'.format(data[t],'\t',t) for t in data))
            else:
                print("Class \t Word types")
                for t in data:
                    print(t, "\t", data[t])

    else:
        
        # It prints the frequency class chosen by the user in 2 corpora
        freqclass1 = data[0]
        freqclass2 = data[1]
        if type(freqclass1) == list and type(freqclass2) == list:
             if tofile.o:
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines("%s\n" % i for i in freqclass1)
                with open(tofile2, 'w') as output_file:
                    output_file.writelines("%s\n" % i for i in freqclass2)
             else:
                 
                print(f1)
                print("Class", value)
                print()
                for t in freqclass1:
                    print(t)
                    
                for s in range(3):
                    print()
                    
                print(f2)
                print("Class", value)
                print()
                for t in freqclass2:
                    print(t)
        else:
            # It prints the frequency classes of the 2 corpora
            if tofile.o:
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {}'.format(freqclass1[t],'\t',t) for t in freqclass1))
                    
                with open(tofile2, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {}'.format(freqclass2[t],'\t',t) for t in freqclass2))
                    
            else:
                print(f1)
                print("Class \t Word types")
                for t in freqclass1:
                    print(t, "\t", freqclass1[t])
                
                for s in range(3):
                    print()
                
                print(f2)
                print("Class \t Word types")
                for t in freqclass2:
                    print(t, "\t", freqclass2[t])


                    
        
# This function prints a graph of the most frequent n words. It requires
# Mathprolib to work
def print_FGraph(freqdist, value, f1, f2, tofile):
    if f2 is None:
        freqdist.plot(value)
    else:
        freqdist1 = freqdist[0]
        freqdist2 = freqdist[1]
        freqdist1.plot(value)
        freqdist2.plot(value)

        
        
# This is the function which prints the result of the commands
# "bigrams". The function takes in input
# the data, which can be a list or a taskpack object, the first corpus,
# the second corpus and the tofile object

def print_bigrams(data, f1, f2, tofile):
   
    if f2 is None:
        if isinstance(data, taskpack) == False:
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {}'.format(b[0],b[1]) for b in data))
            else:
                for b in data:
                    print(b[0], b[1])
        else:
            checktask(data, f1, f2, tofile)
    else:
        
        if type(data) == list:
            B1 = data[0]
            B2 = data[1]
            if tofile.o:
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {}'.format(b[0],b[1]) for b in B1))
                with open(tofile2, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {}'.format(b[0],b[1]) for b in B2))
            else:
                print(f1)
                for b in B1:
                    print(b[0], b[1])
                for s in range(3):
                    print()

                print(f2)
                for b in B2:
                    print(b[0], b[1])
                   
        else:
            checktask(data, f1, f2, tofile)



            
# This function prints the result of the bfreqdist task. 
def print_Bfrequency(data, value, f1, f2, tofile):
    
    if f2 is None:  
        if isinstance(data, taskpack) == False:
            bfreqdist = data
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {} {}'.format(bfreqdist[t],'\t',t[0], t[1]) for t in bfreqdist))
            else:
                print("Freq \t token")
                for t in bfreqdist:
                    print(bfreqdist[t], "\t", t[0], t[1])
        else:
            checktask(data, f1, f2, tofile)
                              
    else:
        if type(data) == list:
            bfreqdist1 = data[0]
            bfreqdist2 = data[1]
            if tofile.o:
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {} {}'.format(bfreqdist1[t],'\t',t[0], t[1]) for t in bfreqdist1))
                with open(tofile2, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {} {}'.format(bfreqdist2[t],'\t',t[0], t[1]) for t in bfreqdist2))
            else:
                print(f1)
                print("Freq \t token")
                for t in bfreqdist1:
                    print(bfreqdist1[t], "\t", t[0], t[1])
                for s in range(3):
                    print()

                print(f2)
                for t in bfreqdist2:
                    print(bfreqdist2[t], "\t", t[0], t[1])
        
         
        else:
            checktask(data, f1, f2, tofile)



            
# This is the function which prints the result of the commands
# "markov". The function takes in input
# the data, which can be a list of tuples or a task object,
# the first corpus, the second corpus and the tofile object

def print_probability(data, f1, f2, tofile):
    
    if f2 is None:  
        if type(data) == list:
            freqprob = data
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {} {}'.format(s[0],'\n',s[1], '\n') for s in freqprob))
            else:
                for s in freqprob:
                    print(s[0])
                    print(s[1])
                    print()

    else:
        if type(data) == list:
            
            freqprob1 = data[0]
            freqprob2 = data[1]
        
            if tofile.o:
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {} {}'.format(s[0],'\n',s[1], '\n') for s in freqprob1))
                with open(tofile2, 'w') as output_file:
                    output_file.writelines('\n'.join('{} {} {} {}'.format(s[0],'\n',s[1], '\n') for s in freqprob2))
                

            else:
                print(f1)
                for s in freqprob1:
                    print(s[0])
                    print(s[1])
                    print()
                for s in range(3):
                    print()

                print(f2)
                for s in freqprob2:
                    print(s[0])
                    print(s[1])
                    print()


                    

# This is the function which prints the result of the commands
# "name_entities". The function takes in input
# the data, which can be a tree object or a taskpack object,
# the first corpus, the second corpus and the tofile object

def print_NEtagging(data, f1, f2, tofile):
    
    if f2 is None:  
        if isinstance(data, taskpack) == False:
            if tofile.o:
                with open(tofile.dest, 'w') as output_file:
                    output_file.writelines(str(data))
            else:
                print(data)
   
        else:
            checktask(data, f1, f2, tofile)

    else:
        if isinstance(data, taskpack) == False:
            ne1 = data[0]
            ne2 = data[1]
        
            if tofile.o:
                tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
                with open(tofile1, 'w') as output_file:
                    output_file.writelines(str(ne1))
                with open(tofile2, 'w') as output_file:
                    output_file.writelines(str(ne2))
                    
            else:
                
                print(f1)
                print(ne1)
                for s in range(3):
                    print()

                print(f2)
                print(ne2)


        else:
            checktask(data, f1, f2, tofile)
                


# This function prints the result of the entfound task. 
def print_entfound(data, f1, f2, tofile):
    
    if f2 is None:  
        if tofile.o:
            with open(tofile.dest, 'w') as output_file:
                output_file.writelines('\n'.join('{} {}'.format(ne[0],ne[1]) for ne in data))
        else:
            print("Word", "\t", "Entity tag")
            for ne in data:
                print(ne[0], "\t", ne[1])

    else:
        
        ne1 = data[0]
        ne2 = data[1]
        if tofile.o:
            tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
            with open(tofile1, 'w') as output_file:
                output_file.writelines('\n'.join('{} {}'.format(e[0],e[1]) for e in ne1))
            with open(tofile2, 'w') as output_file:
                output_file.writelines('\n'.join('{} {}'.format(e[0],e[1]) for e in ne2))
                
        else:
            print(f1)
            print("Word", "\t", "Entity tag")
            for e in ne1:
                print(e[0], "\t", e[1])
            for s in range(3):
                    print()

            print(f2)
            print("Word", "\t", "Entity tag")
            for e in ne2:
                print(e[0], "\t", e[1])
          

                
# This function prints the result of the nodeprint task. 
def print_nodeprint(data, f1, f2, tofile):
    
    if f2 is None:  
        if tofile.o:
            with open(tofile.dest, 'w') as output_file:
                output_file.writelines('\n'.join('{}'.format(e) for e in data))
        else:
            for node in data:
                print(node)

    else:
        
        ne1 = data[0]
        ne2 = data[1]
        if tofile.o:
            tofile1, tofile2 = doublepath(f1, f2, tofile.dest)
            with open(tofile1, 'w') as output_file:
                output_file.writelines('\n'.join('{}'.format(e) for e in ne1))
            with open(tofile2, 'w') as output_file:
                output_file.writelines('\n'.join('{}'.format(e) for e in ne2))
                
        else:
            print(f1)
            for node in ne1:
                print(node)
            for s in range(3):
                    print()

            print(f2)
            for node in ne2:
                print(node)
