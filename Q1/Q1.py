#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# In[2]:


def importDocument(path):
    content = {}
    file_list = []
    for info in os.walk(path):
        filenames = info[2]
        for file in filenames:
            try:
                with open(path+file) as f:
                    lines = f.readlines()
                    content[file] = lines
                    file_list.append(file)
            except:
                print("Discarded file : \t",file)
    return content, file_list


# In[3]:


def onlyWords(documents):
    for key, value in documents.items():
        buff = []
        for line in range(len(value)):
            if len(value[line].strip()) != 0:
                linetoken = nltk.RegexpTokenizer(r"\w+").tokenize(value[line])
                linetoken = [i.lower() for i in linetoken]
                if len(linetoken) != 0:
                    buff.append(linetoken)
        documents[key] = buff
    return documents


# In[4]:


def removeStopWords(documents):
    stop_words = set(stopwords.words('english'))
    for key, value in documents.items():
        for line in range(len(value)):
            value[line] = [i for i in value[line] if not i in stop_words]
        documents[key] = value
    return documents


# In[5]:


def lemmatization(documents):
    lemmatizer = WordNetLemmatizer()
    for key, value in documents.items():
        for line in range(len(value)):
            value[line] = [lemmatizer.lemmatize(i) for i in value[line]]
    return documents


# In[6]:


def uniqueWords(documents):
    unique = []
    content = {}
    for i, t in enumerate(documents.items()):
        value = t[1]
        doc = []
        for line in value:
            doc += line
        doc = list(set(doc))
        unique += doc
        for word in doc:
            if word not in content:
                content[word] = [1,[i+1]]
            else:
                content[word][0] += 1
                content[word][1].append(i+1)
    return list(set(unique)), content


# In[7]:


def removeUnderscore(document, wordslist):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    remove = []
    no_exist = []
    for key in document:
        if not key.isalnum():
            word = key.replace("_"," ").strip()
            word = nltk.RegexpTokenizer(r"\w+").tokenize(word)
            word = [i.lower() for i in word]
            word = [lemmatizer.lemmatize(i) for i in word]
            
            for token in word:
                if len(token) == 0 or token in stop_words:
                    continue
                elif token in wordslist:
                    document[token][0] += document[key][0]
                    document[token][1] =  sorted(list(set(document[token][1]+document[key][1])))
                else:
                    no_exist.append([token,document[key][0], document[key][1]]) 
            remove.append(key)
    
    
    for item in no_exist:
        if item[0] not in document:
            document[item[0]] = [item[1], item[2]]
            wordslist.append(item[0])
        else:
            document[token][0] += document[key][0]
            document[token][1] =  sorted(list(set(document[token][1]+document[key][1])))
        
    for key in remove:
        del document[key]
        wordslist.remove(key)
    
    return wordslist, document


# In[8]:


def queryPreprocess(query):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    linetoken = nltk.RegexpTokenizer(r"\w+").tokenize(query)
    linetoken = [i.lower() for i in linetoken]
    linetoken = [i for i in linetoken if not i in stop_words]
    linetoken = [lemmatizer.lemmatize(i) for i in linetoken]
    return linetoken


# In[9]:


def queryNOT(querylist, size):
    doclist = [0,[]]
    for i in range(size):
        if (i+1) not in querylist[1]:
            doclist[0] += 1
            doclist[1].append(i+1)
    return doclist


# In[10]:


def queryOperation(doclist, word, document, query,size, NOT = False):
    i = 0
    j = 0
    common = [0,[]]
    union = [0,[]] 
    if not NOT:
        querylist = document[word]
    else:
        querylist = queryNOT(document[word],size)
    
#     print(doclist[0])
#     print(document[word][0])
#     print(querylist[0])
    comp = 0
    while i<doclist[0] and j<querylist[0]:
        comp += 1
        if doclist[1][i] < querylist[1][j]:
            union[1].append(doclist[1][i])
            i += 1
        elif doclist[1][i] > querylist[1][j]:
            union[1].append(querylist[1][j])
            j += 1
        else:
            union[1].append(doclist[1][i])
            common[1].append(doclist[1][i])
            common[0] += 1
            i += 1
            j += 1
        union[0] += 1
    
    while i<doclist[0]:
        union[1].append(doclist[1][i])
        union[0] += 1
        i += 1
    
    while j<querylist[0]:
        union[1].append(querylist[1][j])
        union[0] += 1
        j += 1
    
#     print(union[0])
#     print(common[0])
    if query == "OR":
        return union, comp
    else:
        return common, comp


# In[21]:


def compute(query, operation,unique_words_document,size):
    query = queryPreprocess(query)
    doclist = unique_words_document[query[0]]
    comparisons = 0
    for i in range(len(query)-1):
        op = operation[i].split(" ")
        if len(op) == 1:
            doclist, k = queryOperation(doclist,query[i+1],unique_words_document, op[0], size)
        else:
            doclist, k = queryOperation(doclist,query[i+1],unique_words_document, op[0], size, True)
        comparisons += k
        
    print("Number of documents : ",doclist[0])
    print("Number of comparisons : ",comparisons)


# In[11]:


path = "dataset/Humor,Hist,Media,Food/"
documents, files = importDocument(path)
size = len(documents)
print(size)


# In[12]:


documents = onlyWords(documents)
documents = removeStopWords(documents)
documents = lemmatization(documents)


# In[13]:


unique_words, unique_words_document = uniqueWords(documents)
unique_words, unique_words_document = removeUnderscore(unique_words_document, unique_words)


# In[14]:


# query = "lion stood thoughtfully for a moment"
# query = "telephone,paved, roads"
# operation = [ "OR", "OR", "OR" ]
# operation = ["OR NOT", "AND NOT"]


# In[23]:


n = int(input())
for i in range(n):
    query = str(input("Enter query : "))
    operation = list(map(str,input("Enter the operations : ").strip().split(',')))
    print()
    compute(query, operation, unique_words_document, size)
    print()

