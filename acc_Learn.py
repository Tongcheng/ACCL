#!/usr/bin/env python
import nltk
from nltk import tokenize
from nltk.corpus import wordnet

#setting
file_OUTPUT="file_out.html"


##helper_functions
#Input is a sentence(a long string), output word tuple with pos_tag in 2nd position 
def sentence_to_wordProperty(sentence):
    wordList=nltk.word_tokenize(sentence)
    return nltk.pos_tag(wordList)

#helper function for pattern matching 
def helper_PairToPair(a):
        if a[1]=='JJ' or a[1]=='JJR' or a[1]=='JJS':
            return (a[0],'ADJ')
        elif a[1]=='NN' or a[1]=='NNS' or a[1]=='NNP' or a[1]=='NNPS':
            return (a[0],'NOUN')
        elif a[1]=='RB' or a[1]=='RBR' or a[1]=='RBS':
            return (a[0],'ADV')
        else:
            return (a[0],'zardoz')

#the function that maps big tag library to small tag library
def tagMap(tagList_Big):
    return map(helper_PairToPair,tagList_Big)
    
#if 'n' <- 'NOUN', 'a' <- 'ADJ', 'r' <- 'ADV'; else 'e'
def type_string(type0):
    if type0.find('NOUN') !=-1:
        return 'n'
    elif type0.find('ADV') !=-1:
        return 'r'
    elif type0.find('ADJ') !=-1:
        return 'a'
    else:
        return 'e'

#a simple function to write red
def write_red(f, str_):
    f.write('<b style="color:#ff0000">%s</b>' % str_)

#detect the similarity of two strings by looping all the words and return the maximum path_similarity
def word_pair(word1_input,word2_env,type1):
    acc=0
    setS=wordnet.synsets(word1_input,type_string(type1))
    if len(setS)>15:
        return 0
    for i in setS:
        for j in wordnet.synsets(word2_env):
            sim= i.wup_similarity(j)
            if sim>acc:
                acc=sim
    return acc

#test funcition: given a short list of important words, and a long list of wordsPair(second position Tag), generate color
def colorize(file_to,list_imp,list_wordPair):
    for i in list_wordPair:
        if i[1]!='zardoz':
        #flag is 0 then not relevant, 1 then relevant
            flag=0
            acc0=0
            for j in list_imp:
                w_index=word_pair(i[0],j,i[1])
                if w_index>0.4 and w_index>acc0:
                    flag=1
            if flag==1:
                write_red(file_to,i[0])
                file_to.write(' ')
            else:
                file_to.write(i[0])
                file_to.write(' ')
        else:
            file_to.write(i[0])
            file_to.write(' ')
        
#fake data
data_env="computational neuroscience"
data1="""The term "computational neuroscience" was introduced by Eric L. Schwartz, who organized a conference, held in 1985 in Carmel, California, at the request of the Systems Development Foundation to provide a summary of the current status of a field which until that point was referred to by a variety of names, such as neural modeling, brain theory and neural networks. The proceedings of this definitional meeting were published in 1990 as the book Computational Neuroscience.[2] The first open international meeting focused on Computational Neuroscience was organized by James M. Bower and John Miller in San Francisco, California in 1989 and has continued each year since as the annual CNS meeting [3] The first graduate educational program in computational neuroscience was organized as the Computational and Neural Systems Ph.D. program at the California Institute of Technology in 1985.
The early historical roots of the field can be traced to the work of people such as Louis Lapicque, Hodgkin & Huxley, Hubel & Wiesel, and David Marr, to name a few. Lapicque introduced the integrate and fire model of the neuron in a seminal article published in 1907;[4] this model is still one of the most popular models in computational neuroscience for both cellular and neural networks studies, as well as in mathematical neuroscience because of its simplicity (see the recent review article published recently for the centenary of Lapicque's original paper).[5] About 40 years later, Hodgkin & Huxley developed the voltage clamp and created the first biophysical model of the action potential. Hubel & Wiesel discovered that neurons in the primary visual cortex, the first cortical area to process information coming from the retina, have oriented receptive fields and are organized in columns.[6] David Marr's work focused on the interactions between neurons, suggesting computational approaches to the study of how functional groups of neurons within the hippocampus and neocortex interact, store, process, and transmit information. Computational modeling of biophysically realistic neurons and dendrites began with the work of Wilfrid Rall, with the first multicompartmental model using cable
theory."""


#fake main
if __name__=="__main__":
    #open the output file with writing mode
    file_out=open(file_OUTPUT,'w')
    #get a list of sentence
    sentList=tokenize.sent_tokenize(data1)
    #put the html tag to the head of the file
    file_out.write("<html>")
    for s in sentList:
        file_out.write('<p>')
        pairList=tagMap(sentence_to_wordProperty(s))
        colorize(file_out,data_env.split(),pairList)
        file_out.write('</p>')
    #put the end html tag to the tail of the file
    file_out.write("</html>")
    file_out.close()
    