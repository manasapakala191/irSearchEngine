import math
from tokens import *
from fileOperations import *
from invertedIndex import *
import time

class Search:
    def __init__(self, trie_root):
        self.trie_root=trie_root
    
    # tf-idf rating for each word in the query 
    def search_query(self,query,fo,cSize):
        tf_idf={}
        lineStr=""
        idx=self.trie_root.searchTrie(query)
        if idx==-1:
            print(query,"Couldn't find that word")
            # self.trie_root.printTrie(self.trie_root.root,"",0)
            return tf_idf
        else:
            lineStr=fo.readLineFromOutput(idx+1)
            instance = Post.fromString(lineStr)
            df=len(instance.documents)
            idf=math.log(cSize/df)
            print("IDF for the term ",query, " : ","{0:.3f}".format(idf))
            for doc in instance.documents.keys():
                tf=instance.documents[doc]
                tf_idf[doc]=(1+math.log(tf))*idf
            return tf_idf

    # sum of tf-idf scores for all words in the query
    def search_phrasal_query(self,query_tokens,fo,size):
        print(query_tokens)
        scores={}
        for word in query_tokens:
            # add both dicts
            temp_scores=self.search_query(word,fo,size)
            temp={}
            for doc in (scores, temp_scores):
                for key, value in doc.items():
                    if key in temp.keys():
                        temp[key]+=value
                    else:
                        temp[key]=value
                    # print(key, value)
            scores=temp
        i=0
        results={}
        print("No. of blogs found: ",len(scores))
        for doc in sorted(scores, key=scores.get, reverse=True):
            if i<10:
                blog=fo.getTitle(doc)
                blog["@"]=doc[:-5]
                blog["score"]=scores[doc]
                results[doc]=blog
                i+=1
            else:
                break
        # print(results)
        return results
        # return  #docs with maximum score

    # uses a recursive algo in invertedIndex.py -> Trie to build suggestions
    def autoComplete(self,query):
        suggestions=[]
        node=self.trie_root.suggest(query)
        suggestions=[]
        self.trie_root.suggestions(node,query,0,suggestions)
        return suggestions
 

class BuildIndex:
    @staticmethod
    def rebuildIndex(fo,trieRoot,postCollect):
        start = time.time()
        buildIndex(fo,trieRoot,postCollect)
        writeTrie(trieRoot,fo)
        end = time.time()
        print("Time taken to build index: ",end - start)
        return end-start

    @staticmethod
    def searchCLI(fo,trieRoot,docCount):
        searchObj = Search(trieRoot)
        print('Enter query:')
        q = input()
        query_tokens=preprocessQuery(q)
        results=searchObj.search_phrasal_query(query_tokens,fo,docCount)
        print(results)


# uncomment to build index and query from CLI

# fo=FileOperations()
# trieRoot = Trie()
# postCollect=[]
# BuildIndex.rebuildIndex(fo,trieRoot,postCollect)
# docCount=loadTrie(fo,trieRoot)
# BuildIndex.searchCLI(fo,trieRoot,docCount)



        
