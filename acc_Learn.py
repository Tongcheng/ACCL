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
    
        

#a simple function to write red
def write_red(f, str_):
    f.write('<b style="color:#ff0000">%s</b>' % str_)

#detect the similarity of two strings by looping all the words and return the maximum path_similarity
def word_pair(word1_input,word2_env):
    acc=0
    for i in wordnet.synsets(word1_input):
        for j in wordnet.synsets(word2_env):
            sim= i.path_similarity(j)
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
                w_index=word_pair(i[0],j)
                if w_index>0.1 and w_index>acc0:
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
data_env="finance"
data1="""Finance is a field that deals with the allocation of assets and liabilities over time under conditions of certainty and
uncertainty. Finance also applies and uses the theories of economics at some level. Finance can also be defined as the science of money management. A key point in finance is the time value of money, which states that p
urchasing power of one unit of currency can vary over time. Finance aims to price assets based on their risk level and their expected rate of return. Finance can be broken into three different sub-categories: public finance,
corporate finance and personal finance."""


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
    