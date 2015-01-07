# -*- coding: utf8 -*-
#!/usr/bin/env python
import wikipedia
import nltk
from nltk import tokenize
from sets import Set
from bannedWordList import bannedDict

####  General  ####
#general idea: go through the text twice
#First loop:
#Structure1: Current_phrase(set of phrases/strings)
#Structure2: Potential_phrase(set of phrases/strings)
#Structure3: Word_to_Phrase(dictionary of word:potential_Phrase)
#Structure4: BannedWordSet(Set of words)
#Second Loop:
#Structure1: Current_phrase(set of phrases/strings)
#Structure2: Word_to_Phrase_v2(only about current phrase)
#setting
file_OUTPUT="file_out.html"

#helper functions
##add a single url to the potential set
##url0 is a url, which in our format is unicode
##have a lot of side effects, but return nothing
def urlAddition(cur_set,pot_set,dict0,url0):
    #test
    #print 'adding url'+`url0`
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


if __name__=="__main__":
    #initialize the dictionary
    f_in=open("file_in.txt","r")
    data1=f_in.read()
    data1.replace("\n","")
    f_env=open("file_env.txt","r")
    data_envS=f_env.read()
    data_env=nltk.word_tokenize(data_envS)
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
            if dict_index.get(w1.lower())==None:
                dict_index[w1.lower()]=[]
            #append the phrase to the value of words anyway
            dict_index[w1.lower()].append(ph)
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
            if not dict_index.get(w1.lower()) ==None:
                phList=dict_index[w1.lower()]
                flag=False
                for ph in phList:
                    if ph.lower() in s.lower():
                        flag=True
                if flag and (not w1.lower() in bannedDict):
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
    print 'index dictionary is '+`dict_index`
    file_out.write("</html>")
    file_out.close()
