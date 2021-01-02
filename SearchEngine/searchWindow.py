from tkinter import *
from query import *

root = Tk() 

root.title(" Search Blogs ") 

fram = Frame(root) 

fo=FileOperations()
trieRoot = Trie()
docCount=loadTrie(fo,trieRoot)
searchObj = Search(trieRoot)


Label(fram,text='Query:').pack(side=LEFT) 

edit = Entry(fram)  
edit.pack(side=LEFT, fill=BOTH, expand=1) 

edit.focus_set() 

buttonIndex = Button(fram, text='Build Index') 
buttonIndex.pack(side=RIGHT,padx=5)

butt = Button(fram, text='Search') 
butt.pack(side=RIGHT)
fram.pack(side=TOP,padx=10,pady=10) 


buttonComplete = Button(fram, text='Auto Complete Words') 
buttonComplete.pack(side=RIGHT,padx=5)


text = Text(root) 

text.pack(side=BOTTOM,padx=10,pady=10) 

text.tag_configure('biggest', font=('Verdana', 12, 'bold'))
text.tag_configure('big', font=('Verdana', 10, 'bold'))
text.tag_configure('bold_italics', font=('Arial', 9, 'bold'))
text.tag_configure('color',
                    foreground='#476042',
                    font=('Tempus Sans ITC', 8, 'bold'))
text.tag_configure('color1',
                    font=('Tempus Sans ITC', 8, 'bold'))


searchResults={}
def search():
    query = edit.get()
    text.delete('1.0', END)
    if query:
        query_tokens=preprocessQuery(query)
        searchResults=searchObj.search_phrasal_query(query_tokens,fo,docCount)
        text.insert(END,"Top 10 blogs: \n",'biggest')
        for doc,blog in searchResults.items():
            text.insert(END,"\n"+blog["title"],'big')
            text.insert(END,"\nAuthor: "+blog["author"],'bold_italics')
            text.insert(END,"\n"+" @: "+blog["@"],'color')
            text.insert(END,"\nTf-Idf Score: "+str(blog["score"]),'color1')
            text.insert(END,"\n")
def complete():
    query = edit.get()
    text.delete('1.0', END)
    # text.insert(END,query+" Suggestions:",'color1')
    if query:
        query_tokens=query.split(' ')
        text.insert(END,query+" Suggestions: \n",'biggest')
        suggestions=searchObj.autoComplete(query_tokens[-1])
        for i in suggestions:
            text.insert(END,i+" \n",'bold_italics')


def buildInvertedIndex():
    trieRoot = Trie()
    postCollect=[]
    time=BuildIndex.rebuildIndex(fo,trieRoot,postCollect)
    text.delete('1.0', END)
    text.insert(END,"Time taken to build index: "+str(time)+" seconds",'biggest')
    docCount=loadTrie(fo,trieRoot)


butt.config(command=search) 
buttonComplete.config(command=complete)
buttonIndex.config(command=buildInvertedIndex)
 
root.mainloop() 
