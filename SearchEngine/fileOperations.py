import os, json
import json
import linecache


# All file related operations(reads, writes) are in this class
class FileOperations:
    def __init__(self):
        self.path = '../dataset/dataset'
        self.docCount=0

    def readFiles(self,num):
        i=0
        wordList={}
        json_files = [pos_json for pos_json in os.listdir(self.path+str(num))]
        for file_json in json_files:
            if i<10000:
                path_file=self.path+str(num)+'/'+file_json
                with open(path_file,encoding="utf8") as fil:
                    # print(path_1+'/'+file_json)
                    data=json.load(fil)
                    wordList[path_file[11:]]=data["text"]
                    self.docCount+=1
                    i+=1
        return wordList

    def readLineFromOutput(self,num):
        return linecache.getline('output.txt', num)
    
    def getTitle(self,filePath):
        blog={}
        path_file=self.path+filePath[7:]
        with open(path_file,encoding="utf8") as fil:
            # print(path_1+'/'+file_json)
            data=json.load(fil)
            blog["title"]=data["title"]
            blog["author"]=data["author"]
        return blog

    def writeTrieFile(self,wordsList):
        wordsList["#docCount"]=self.docCount
        with open('trie.txt', 'w') as fil:
            fil.write(json.dumps(wordsList))
    
    def readTrieFile(self):
        with open('trie.txt') as fil: 
            data = fil.read()
        wordsList = json.loads(data)
        return wordsList

    def writePostingListFile(self,postCollect):
        fil = open("output.txt", "w")
        for word in postCollect:
            fil.write(str(word))
        fil.close()