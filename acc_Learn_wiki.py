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

#deprecated
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
data_env=["oxygen"]
data1="""
Oxygen is a chemical element with symbol O and atomic number 8. It is a member of the chalcogen group on the periodic table and is a highly reactive nonmetallic element and oxidizing agent that readily forms compounds (notably oxides) with most elements.[1] By mass, oxygen is the third-most abundant element in the universe, after hydrogen and helium.[2] At STP, two atoms of the element bind to form dioxygen, a diatomic gas that is colorless, odorless, and tasteless, with the formula O
2.

Many major classes of organic molecules in living organisms, such as proteins, nucleic acids, carbohydrates, and fats, contain oxygen, as do the major inorganic compounds that are constituents of animal shells, teeth, and bone. Most of the mass of living organisms is oxygen as it is a part of water, the major constituent of lifeforms (for example, about two-thirds of human body mass). Elemental oxygen is produced by cyanobacteria, algae and plants, and is used in cellular respiration for all complex life. Oxygen is toxic to obligately anaerobic organisms, which were the dominant form of early life on Earth until O
2 began to accumulate in the atmosphere. Free elemental O
2 only began to accumulate in the atmosphere about 2.5 billion years ago during the Great Oxygenation Event, about a billion years after the first appearance of these organisms.[3][4] Diatomic oxygen gas constitutes 20.8% of the volume of air.[5] Oxygen is the most abundant element by mass in the Earth's crust as part of oxide compounds such as silicon dioxide, making up almost half of the crust's mass.[6]

Oxygen is an important part of the atmosphere, and is necessary to sustain most terrestrial life as it is used in respiration. However, it is too chemically reactive to remain a free element in Earth's atmosphere without being continuously replenished by the photosynthetic action of living organisms, which use the energy of sunlight to produce elemental oxygen from water. Another form (allotrope) of oxygen, ozone (O
3), strongly absorbs UVB radiation and consequently the high-altitude ozone layer helps protect the biosphere from ultraviolet radiation, but is a pollutant near the surface where it is a by-product of smog. At even higher low earth orbit altitudes, atomic oxygen is a significant presence and a cause of erosion for spacecraft.[7] Oxygen is produced industrially by fractional distillation of liquefied air, use of zeolites with pressure-cycling to concentrate oxygen from air, electrolysis of water and other means. Uses of elemental oxygen include the production of steel, plastics and textiles, brazing, welding and cutting of steels and other metals, rocket propellant, oxygen therapy and life support systems in aircraft, submarines, spaceflight and diving.

"""

if __name__=="__main__":
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
    ##first loop##
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
    print 'starting second loop'
    ##second loop##
    #initialize a new index dictionary
    dict_index={}
    #convert cur_set to index dictionary
    #for each phrase in cur_set
    for ph in current_set:
        #decompose into list of words
        wordList=nltk.word_tokenize(ph)
        #for each word
        for w1 in wordList:
            #if the word not yet in the dictionary, add this key
            if dict_index.get(w1)==None:
                dict_index[w1]=[]
        #append the phrase to the value of words anyway
        dict_index[w1].append(ph)
    #writing preparation
    file_out=open(file_OUTPUT,'w')
    file_out.write("<html>")
    #for each sentence
    for s in sentList:
        file_out.write("<p>")
        wordList=nltk.word_tokenize(s)  
        #for each word in sentence
        for w1 in wordList:
            #if the word is in index dictionary get all the corresponding phrases
            if not dict_index.get(w1) ==None:
                phList=dict_index[w1]
                flag=False
                for ph in phList:
                    if ph.lower() in s.lower():
                        flag=True
                if flag:
                    write_red(file_out,w1)
                    file_out.write(' ')
                else:
                    file_out.write(w1)
                    file_out.write(' ')
            #if any of the phrase in a substring of this sentence, then color it
            else:
                file_out.write(w1)
                file_out.write(' ')
        file_out.write("</p>")
    
    file_out.write("</html>")
    file_out.close()
