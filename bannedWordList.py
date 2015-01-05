from sets import Set
#a set of banned words

#set I: because the words are so frequent that they are not "terms"
partI=Set(["the","a","of","to","from","and","in","is","was","you","are","were","will"
           ,"for","that","this","or","it","as"])
#set II: because the words are wikipedia-specific that are banned
partII=Set(["disambiguation","(",")"])
#complete set
bannedDict=partI.union(partII)
