# -*- coding: utf8 -*-
#!/usr/bin/env python
import wikipedia
import nltk
from nltk import tokenize
from sets import Set
from bannedWordList import bannedDict

####  General  ####
#general idea: go through the text twice
#maintain two things:1. current set; 2. potential set
#first traversal:
#if a word is in potential set and but not in current set,
#add the word to current set
#and union the set of words "related word", into potential set
#second traversal:
#if a word is in current set, mark it "red", (Or show the continuous change of color)
####  Weakness ####
#word is atomic, cannot search for short_phrases
#Struc1: Current_phrase(set of phrases/strings)
#Struc2: Potential_phrase(set of phrases/strings)
#Struc3: Word_to_Phrase(dictionary of word:Phrase)
#Struc4: BannedWordSet(Set of words)

#setting
file_OUTPUT="file_out.html"

#helper functions
##add a single url to the potential set
##url0 is a url, which in our format is unicode
##have a lot of side effects, but return nothing
def urlAddition(cur_set,pot_set,dict0,url0):
    #test
    print 'adding url'+`url0`
    #convert unicode to string(ascii)
    phrase0=url0.encode('ascii','ignore')
    pot_set.add(phrase0)
    wordList0=nltk.word_tokenize(phrase0)
    for word0 in wordList0:
        #if it is not a banned word
        if word0 not in bannedDict:
            #initialize a new word
            if dict0.get(word0)==None:
                dict0[word0]=[]
            if dict0[word0].count(phrase0)==0:    
                dict0[word0].append(phrase0)
    return
#elevate phrase0, add all the related url using urlAddition
def phraseElevation(cur_set,pot_set,dict0,phrase0):
    #test
    print 'trying to elevate phrase'+`phrase0`
    if phrase0 in pot_set:
        cur_set.add(phrase0)
        wordList0=nltk.word_tokenize(phrase0)
        #parse it into words, and remove all correlations
        for word0 in wordList0:
            if not dict0.get(word0)==None:
            #if the this word is in dictionary, then remove all occurences of phrase in its value
                valList=dict0[word0]
                while valList.count(phrase0)>0:
                    valList.remove(phrase0)
                dict0[word0]=valList
        try:
            thisPage=wikipedia.page(phrase0)
            for i in thisPage.links:
                urlAddition(cur_set,pot_set,dict0,i)
        except:
            return
    else:
        return

#clean the dict0 set
def clean_dict(dict0,num):
    output={}
    for i in dict0:
        if len(dict0[i])>=num:
            output[i]=dict0[i]
    return output


#determination function, true if type is NN,NNS,NNP,NNPS,JJ,JJR,JJS,RB,RBR,RBS
def determineWord(inputString):
    if inputString=="NN" or inputString=="NNS" or inputString=="NNP" or inputString=="NNPS" or inputString=="JJ" or inputString=="JJR" or inputString=="JJS" or inputString=="RB" or inputString=="RBR" or inputString=="RBS":
        return True
    return False

#a simple function to write red
def write_red(f, string0):
    f.write('<b style="color:#ff0000">%s</b>' % string0)



#fake data
data_env=["computational","neuroscience"]
data1="""The term "computational neuroscience" was introduced by Eric L. Schwartz, who organized a conference, held in 1985 in Carmel, California, at the request of the Systems Development Foundation to provide a summary of the current status of a field which until that point was referred to by a variety of names, such as neural modeling, brain theory and neural networks. The proceedings of this definitional meeting were published in 1990 as the book Computational Neuroscience.[2] The first open international meeting focused on Computational Neuroscience was organized by James M. Bower and John Miller in San Francisco, California in 1989 and has continued each year since as the annual CNS meeting [3] The first graduate educational program in computational neuroscience was organized as the Computational and Neural Systems Ph.D. program at the California Institute of Technology in 1985.
The early historical roots of the field can be traced to the work of people such as Louis Lapicque, Hodgkin & Huxley, Hubel & Wiesel, and David Marr, to name a few. Lapicque introduced the integrate and fire model of the neuron in a seminal article published in 1907;[4] this model is still one of the most popular models in computational neuroscience for both cellular and neural networks studies, as well as in mathematical neuroscience because of its simplicity (see the recent review article published recently for the centenary of Lapicque's original paper).[5] About 40 years later, Hodgkin & Huxley developed the voltage clamp and created the first biophysical model of the action potential. Hubel & Wiesel discovered that neurons in the primary visual cortex, the first cortical area to process information coming from the retina, have oriented receptive fields and are organized in columns.[6] David Marr's work focused on the interactions between neurons, suggesting computational approaches to the study of how functional groups of neurons within the hippocampus and neocortex interact, store, process, and transmit information. Computational modeling of biophysically realistic neurons and dendrites began with the work of Wilfrid Rall, with the first multicompartmental model using cable
theory."""

if __name__=="__main__":
    #stub_pre
    file_out=open(file_OUTPUT,'w')
    file_out.write("<html>")
    #initialize the dictionary
    dict_WP={}
    #initialize current set and potential set
    current_set=Set(data_env)
    #initialize the potential set
    potential_set=Set([])
    for i in current_set:
        try:
            thePage=wikipedia.page(i)
            for j in thePage.links:
                urlAddition(current_set,potential_set,dict_WP,j)
        except:
            pass
    #get a list of sentence
    print "initial size is"+`len(dict_WP)`
    #dict_WP=clean_dict(dict_WP,5)
    sentList=tokenize.sent_tokenize(data1)
    #main part
    #first loop
    #asd=0#test
    for s in sentList:
        wordListAlpha=nltk.word_tokenize(s)
        #a list of pair of (word,type)
        typePairList=nltk.pos_tag(wordListAlpha)
        for pair in typePairList:
            #print 'asd='+`asd`
            #asd=asd+1
            #print pair[0]
            #print 'dict0 len is '+`len(dict_WP)`
            if determineWord(pair[1]):
                #see if the dict_WP(dict0) has this word
                if not dict_WP.get(pair[0])==None:
                    #elevate each related phrase
                    for phraseAlpha in dict_WP.get(pair[0]):
                        #conditional constraint: elevate a phrase if it is a substring of the sentence
                        if (phraseAlpha.lower() in s.lower()) and (phraseAlpha not in current_set):
                            phraseElevation(current_set,potential_set,dict_WP,phraseAlpha)
                            #dict_WP=clean_dict(dict_WP,5)
    
    print 'cur_set is '+`current_set`
    print 'pot_set length is '+`len(potential_set)`
    #print 'dict0 is '+`dict_WP`
    #second loop
    
    
    
    file_out.close()
