import collections
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.porter import *
import gensim


class Token:
    def __init__(self,docdict):
        self.docdict=docdict

    def tokenize(self):
        tokenizer = RegexpTokenizer(r'[0-9]{4}|[a-zA-Z]{3,}')
        all_tokens=[]
        doc_tokens = collections.defaultdict(list)
        for doc in self.docdict.keys():
            doc_tokens[doc]=tokenizer.tokenize(self.docdict[doc].lower())
        return doc_tokens

    def filterStopWords(self):
        stopwords = getStopWords()
        doc_tokens = collections.defaultdict(list)
        tokenizedDocs=self.tokenize()
        for doc in tokenizedDocs.keys():
            doc_tokens[doc]=list(filter(lambda x: x not in stopwords,tokenizedDocs[doc]))
        return doc_tokens
    
    def stemTokens(self):
        stemmer = PorterStemmer()
        i=0
        filteredDocs=self.filterStopWords()
        doc_tokens=collections.defaultdict(list)
        for doc in filteredDocs.keys():
            doc_tokens[doc]=[gensim.parsing.stem_text(token) for token in filteredDocs[doc]]
        return doc_tokens

def getStopWords():
        ca = stopwords.words("english")
        ca = set(ca)
        return ca

def preprocessQuery(query):
    tokenizer = RegexpTokenizer(r'[0-9]{4}|[a-zA-Z]{3,}')
    q_tokens=tokenizer.tokenize(query.lower())
    stopwords = getStopWords()
    q_tokens=list(filter(lambda x: x not in stopwords,q_tokens))
    q_tokens=[gensim.parsing.stem_text(token) for token in q_tokens]
    return q_tokens


# fo=FileOperations()
# docdict=fo.readFiles()
# tokenObj = Token(docdict)
# tokens=tokenObj.stemTokens()



