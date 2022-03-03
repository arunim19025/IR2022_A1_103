# -*- coding: utf-8 -*-


#The location of the database
database = "/content/drive/MyDrive/Humor,Hist,Media,Food"

#Imports used
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

#Define the stop words
stop_words = set(stopwords.words('english'))

#This function is used to preprocess the text
def preprocess(text):
    #Convert text to lower
    text = text.lower()

    #Remove punctuations
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    arr = tokenizer.tokenize(text)

    #Remove the stop words
    arr = [w for w in arr if not w in stop_words]

    #The spaces are removed in tokenisation function

    return arr

#This creates positional index
#Input are the gloabl dictionary "pos_idx",The tokenised "arr" and the current document number (doc_num)
def createPositionalIndex(arr,pos_idx,doc_num):
    for pos,term in enumerate(arr):
        if term in pos_idx:
            pos_idx[term][0] += 1                          #update the frequency of the word

            if doc_num in pos_idx[term][1]:
                pos_idx[term][1][doc_num].append(pos)      #if the doc_num of the word exist add the position
            else:
                temp_list = [pos]
                pos_idx[term][1][doc_num] = temp_list      #if the doc_num of the word doestnt exist create it
        else:
            temp_list = [1,{doc_num: [pos]}]
            pos_idx[term] = temp_list                      #if the term doesnt exist, initialise the frequency and the dictionary

import os
# assign directory
directory = database
pos_idx = {}            #This stores the positional index
doc_num = 0
file_dic = {}           #This stores the file names as value and doc_num as key
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):

        file1 = open(f,errors="ignore") 

        text = file1.read()
        
        #Preprocess
        arr = preprocess(text)

        #Create positional index
        createPositionalIndex(arr,pos_idx,doc_num)
        
        #Assign Doc_num to file name
        file_dic[doc_num] = f
        doc_num += 1

        file1.close()



#--------------------------------------Query--------------------------------#
query = input()
result = {}
count = 0
query_arr = preprocess(query)  #This processes the query
def find_doc(query):
    global result
    global count
    for word in query:
        try:
            current_dic = pos_idx[word][1]
        except:
            print("No doc found")
            break
        if(len(result) == 0):
            result = current_dic 
        else:
            set_result = set(result.keys())
            common_docs = set_result.intersection(set(current_dic.keys()))      #This is the intersection of docs between the final resultant 
            dic = {}                                                            #dictionary and the current selected word docs
            for doc_id in common_docs:
                dic[doc_id] = result[doc_id]
            if(len(common_docs)) == 0:
                print("No doc found")
                break
            result = dic                                                        #This is the resultant based on the same docs
            for doc_id in common_docs:
                #iterate over the posting list
                
                inc_list = [x+count for x in result[doc_id]]
                temp_pos = set(current_dic[doc_id]).intersection(set(inc_list)) #This finds the position in accordance to query
            
                if len(temp_pos) == 0:                                          #if No position is found for the current word in the doc, delete it
                    del result[doc_id]
            
        count += 1



find_doc(query_arr)             #Calling the function

print(result)

names = []
for key in result.keys():
    print(key)
    names.append(file_dic[key])

print("The number of docs found are ",len(names))

print(names)

