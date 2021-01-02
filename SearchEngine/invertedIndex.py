import collections
from tokens import *

class invertedIndex :

    def createTriePostingLists(self,docWordDict,trieRoot,postCollect):
        for doc in docWordDict.keys():
            trieRoot.addListToTrie(docWordDict[doc], doc, postCollect, 0)

    # for each seperate block of the dataset a different inverted Index: made in
    # the ram -> merged with the one in the output file -> cleared from RAM
    def clearReadWrite(self,postCollect, fOpr, trieRoot, num):
        size = len(postCollect)
        array = [Post(postCollect[i].word,0,collections.OrderedDict()) for i in range(0,size)]
        # array=[None]*size
        postCollect.clear()
        postCollect=array
        docdict=fOpr.readFiles(num)
        tokenObj = Token(docdict)
        docWordDict=tokenObj.stemTokens()
        self.createTriePostingLists(docWordDict,trieRoot,postCollect)
        postCollectCopy = self.readpostCollectFromFile()
        self.mergeLists(postCollect, postCollectCopy)
        print("length of merged posting lists: ",len(postCollect))
        fOpr.writePostingListFile(postCollect)
        return postCollect

    # the invertedIndex in the output file and that formed in the RAM are merged
    # here
    def mergeLists(self,postCollect, postCollectCopy):
        # iterate both and merge
        print("merging posting lists from blocks")
        for i in range(len(postCollectCopy)): # already empty instances in post collect
            inst2 = postCollectCopy[i]
            if (postCollect[i]):
                inst1 = postCollect[i]
                inst1.docFreq = inst1.docFreq + inst2.docFreq
                inst1.documents.update(inst2.documents)
                postCollect[i]=inst1
            else:
                postCollect[i]=inst2

    # the invertedIndex is parsed to Post objects here
    def readpostCollectFromFile(self):
        postCollect = []
        file1 = open('output.txt', 'r') 
        Lines = file1.readlines()
        file1.close()
        for line in Lines:
            postCollect.append(Post.fromString(line))
        return postCollect

# a custom class for convenience in building the Inverted Index
class Post:
    def __init__(self,word,docFreq,documents):
        self.word=word # string
        self.docFreq=docFreq # int 
        self.documents = documents # ordered dict

    #  constructor for parsing str back to an object
    @classmethod
    def fromString(cls, objStr):
        index0 = 0
        index1 = 0
        index0 = objStr.index("(")
        index1 = objStr.index(")")
        word = objStr[0: index0]
        docFreq = int(objStr[index0 + 1: index1])
        docs = objStr[index1 + 5:]
        documents = cls.stringtoMap(cls,docs)
        return cls(word,docFreq,documents)

    def stringtoMap(self,mapStr):
        docs = collections.OrderedDict()
        mapStr = mapStr[1:len(mapStr) - 2]
        keyValuePairs = mapStr.split(",")
        flag=0
        for pair in keyValuePairs:
            entry = pair.split(":")
            if flag==0:
                docs[entry[0].strip()[1:len(entry[0])-1]]=int(entry[1].strip())
                flag=1
            else:
                docs[entry[0].strip()[1:len(entry[0])-2]]=int(entry[1].strip())
        return docs # returns ordered dict

    def addDocFreq(self,docName):
        if docName in self.documents.keys():
            self.documents[docName]=self.documents[docName]+1
        else:
            self.docFreq+=1
            self.documents[docName]=1

    def __str__(self):
        return self.word + "(" + str(self.docFreq) + ") => " + str(dict(self.documents)) + "\n"

#  The node of a trie
class Node:
    def __init__(self):
        self.isEnd=False
        self.letters=[None] * 36
        # = [Node() for i in range(36)]
        self.index=-1

    #  updates the index of the end node to make it point to the index at which it
    #  is stored in the list
    def endWord(self,word, docName, postCollect, flag):
        if (self.index == -1):
            instance = Post(word,0,collections.OrderedDict())
            self.index = len(postCollect)
            instance.addDocFreq(docName)
            postCollect.append(instance)
        else:
            if (flag == 1):
                instance = Post(word,0,collections.OrderedDict())
                instance.addDocFreq(docName)
                postCollect[self.index]=instance
            else:
                instance = postCollect[self.index]
                instance.addDocFreq(docName)

#  Trie's root and all trie related operations(add,search,print) are in this
class Trie:

    def __init__(self):
        self.root=Node()

    #  as of now the trie adds alphabets and numbers
    def addtoTrie(self,word, docName, postCollect, flag):
        k = self.root
        c = '1'
        wordT = ""
        for i in range(len(word)):
            c = word[i]
            idx = -1
            if (c.isalpha()):
                idx = ord(c) - ord('a')
            elif(c.isdigit()):
                idx = ord(c) - ord('0') + 26
            if (idx != -1 and idx < 36):
                if(not k.letters[idx]):
                    k.letters[idx] = Node()
                wordT = wordT + c
                k = k.letters[idx]
        k.isEnd = True
        k.endWord(wordT, docName, postCollect, flag)
    
    # adds word to trie while loading from trie.txt
    def addWord(self,word,index):
        k = self.root
        c = '1'
        wordT = ""
        for i in range(len(word)):
            c = word[i]
            idx = -1
            if (c.isalpha()):
                idx = ord(c) - ord('a')
            elif(c.isdigit()):
                idx = ord(c) - ord('0') + 26
            if (idx != -1 and idx < 36):
                if(not k.letters[idx]):
                    k.letters[idx] = Node()
                wordT = wordT + c
                k = k.letters[idx]
        k.isEnd = True
        k.index=index

    def load(self,wordsList):
        print("No. of tokens in trie: ",len(wordsList))
        for word,index in wordsList.items():
            self.addWord(word,index)

    def printTrie(self,k,string,lvl):
        if (k.isEnd):
            print(string,k.index)
        for i in range(36):
            temp = string
            if (k.letters[i]):
                if (i < 26):
                    string = string + chr(i + ord('a'))
                else:
                    string = string + chr(i - 26 + ord('0'))
                self.printTrie(k.letters[i], string, lvl + 1)
                string = temp

    # parsing trie before writing to file
    def writeTrie(self,k,string,lvl,wordsList):
        if (k.isEnd):
            wordsList[string]=k.index
        for i in range(36):
            temp = string
            if (k.letters[i]):
                if (i < 26):
                    string = string + chr(i + ord('a'))
                else:
                    string = string + chr(i - 26 + ord('0'))
                self.writeTrie(k.letters[i], string, lvl + 1,wordsList)
                string = temp

    # implements search in trie and returns index of posting list
    def searchTrie(self,word):
        k = self.root
        for i in  range(len(word)):
            c = word[i]
            idx = -1
            if (c.isalpha()):
                idx = ord(c) - ord('a')
            elif (c.isdigit()):
                idx = ord(c) - ord('0') + 26
            if (idx != -1 and idx < 36):
                if (not k.letters[idx]):
                    return -1
                k = k.letters[idx]
        if (k.isEnd):
            return k.index
        return -1
    
    def suggestions(self,k,string,lvl,slist):
        if k:
            if (k and k.isEnd):
                slist.append(string)
                # print(string,k.index)
            for i in range(36):
                temp = string
                if(k.letters[i]):
                    if (i < 26):
                        string = string + chr(i + ord('a'))
                    else:
                        string = string + chr(i - 26 + ord('0'))
                    self.suggestions(k.letters[i], string, lvl + 1,slist)
                    string = temp


    def suggest(self,query):
        k = self.root
        for i in  range(len(query)):
            c = query[i]
            idx = -1
            if (c.isalpha()):
                idx = ord(c) - ord('a')
            elif (c.isdigit()):
                idx = ord(c) - ord('0') + 26
            if (idx != -1 and idx < 36):
                if (not k.letters[idx]):
                    return None
                k = k.letters[idx]
        return k

    def addListToTrie(self,wordList,docName, postCollect,flag):
        for string in wordList:
            self.addtoTrie(string, docName, postCollect, flag)


def buildIndex(fo,trieRoot,postCollect):
    docdict=fo.readFiles(1)
    tokenObj = Token(docdict)
    docWordDict=tokenObj.stemTokens()
    invIdx=invertedIndex()
    invIdx.createTriePostingLists(docWordDict, trieRoot, postCollect)
    fo.writePostingListFile(postCollect)
    postCollect=invIdx.clearReadWrite(postCollect, fo, trieRoot, 2)

def writeTrie(trieRoot, fo):
    wordsList={}
    print("Writing trie to trie.txt")
    trieRoot.writeTrie(trieRoot.root,"",0,wordsList)
    fo.writeTrieFile(wordsList)

def loadTrie(fo,trieRoot):
    wordsList=fo.readTrieFile()
    print("Loading trie from trie.txt")
    docCount=wordsList["#docCount"]
    del wordsList["#docCount"]
    trieRoot.load(wordsList)
    return docCount


