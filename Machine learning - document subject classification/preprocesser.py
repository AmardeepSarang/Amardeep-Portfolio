"""
-------------------------------------------------------
preprocesser.py
[description of functions]
-------------------------------------------------------
Author:  Amardeep Sarang
ID: 160112080
Email:  sara2080@mylaurier.ca
__updated__ = "2018-11-10"
-------------------------------------------------------
"""
import string
import random
import math
from cgi import log
def gen_names():
    #generate file names
    f_names=[]
    for i in range(1,11):
        s='tech_'+str(i)+'.txt'
        f_names.append(s)
        
    for i in range(1,11):
        s='food_'+str(i)+'.txt'
        f_names.append(s)
    for i in range(1,11):
        s='business_'+str(i)+'.txt'
        f_names.append(s)
    for i in range(1,11):
        s='politics_'+str(i)+'.txt'
        f_names.append(s)
    
    return f_names
def test():
    n=gen_names()
    
    base_feature_set=build_base_feature_set(n)
    print("Base feature set created!")
    #feature_set=base_feature_set
    #change the following functions to change the type of preprocessing
    #-------------------------------------------------------------------------------------
    feature_set=remove_stop_word('stopwords_3.txt', base_feature_set)
   # feature_set=random_feature_select(feature_set, 1000)
    #-------------------------------------------------------------------------------------
    
    i=idf(n, feature_set)
    print(i)
    
def has_num(s):
    return any(i.isdigit() for i in s)
    
def file_to_array(f_name):
    #reads each word in a file into an array
    topic=-1
    f=open(f_name,"r")
    word_list=[]
    for line in f:
        if topic==-1:
            topic=int(line.strip())#get first line
        else:
            words=line.split(" ")
            
            
            for i in range(len(words)):
                word=words[i].strip()
                word=clean_word(word)
                word.strip()
                word=word.lower()# to lower case
                if not word.isspace() and len(word)>0 and has_num(word)==False:
                    word_list.append(word)
    
    f.close()
    return topic, word_list
def clean_word(word):
    l=len(word)
    #remove punctuation
    punct=string.punctuation+'.‘’“”\n'
    
    while (len(word)>0) and (word[l-1] in punct or word[l-1] not in string.printable or word[0] in punct or word[0] not in string.printable):
    
        if word[l-1] in punct or word[l-1] not in string.printable:
            word=word[:l-1]
            
        if len(word)>0:
            if word[0] in punct or word[0] not in string.printable:
                word=word[1:]
                  
        l=len(word)
    return word
def build_base_feature_set(name_array):  
    feature_set=[]
    for name in name_array:
        topic,f_words=file_to_array(name) 
        #if a new word is found add it to feature set
        for word in f_words:
            if word not in feature_set:
                feature_set.append(word)
                
    return feature_set

def remove_stop_word(f_name, base_set):
    #get stop  words from file
    f=open(f_name,"r")
    stop_words=[]
    for line in f:
        line=line.strip()
        line=line.lower()
        stop_words.append(line)
    f.close()
    
    #add non stop words to new feature set
    new_set=[]
    for word in base_set:
        if word not in stop_words:
            new_set.append(word)
            
    return new_set
def random_feature_select(feature_set,n):
    new_set=[]
    #select n random words and add them to new set
    while len(new_set)!=n:
        word=random.choice(feature_set)
        if word not in new_set:
            new_set.append(word)

    return new_set
def feature_set_stats(feature_set,data_num):
    #prints feature set stats
    lines=[]
    f_dis=input("Feature description: ")
    lines.append("Feature description: "+f_dis)
    lines.append("Number of feature in set: "+str(len(feature_set)))
    i=0

    lines.append("index - feature word -  domain")
    for word in feature_set:
        lines.append(str(i)+" - "+word+" - 0-1")
        i=i+1
    lines.append(str(i)+" - 1,2,3,4 key: Tech=1, politics=2, business=3 food=4")
    #create file and print
    fname="dataset_"+str(data_num)+"_feature_description.txt"
    f=open(fname,"x")
    for line in lines:
        f.write(line+"\n")
    f.close
    
def create_dataset(f_names, feature_set, data_num,idf_list):
    fname="dataset_"+str(data_num)+".txt"
    f=open(fname,"x")
    for f_name in f_names:
        #
        topic,word_list=file_to_array(f_name)
        #initialize word count list to 0s
        word_count=[]
        
        for w in feature_set:
            word_count.append(0)
            
        #if the word from the word list is found in the feature set incerment that index in word count
        
        for word in word_list:
            if word in feature_set:
                i=feature_set.index(word)
                word_count[i]=word_count[i]+1
        
        
        #print ration to file
        write_string=""
        i=0
        for count in word_count:
            word_ratio=round(count/len(word_list)*idf_list[i],4)
            i+=1
            write_string=write_string+str(word_ratio)+","
        write_string=write_string+str(topic)+"\n"
        #print("write "+ str(len(word_count)))
        f.write(write_string)
    f.close()
def idf(f_names, feature_set):
    word_array=[]
    for f_name in f_names:
        #create word array
        topic,word_list=file_to_array(f_name)
        word_array.append(word_list)
    
    idf_list=[]
    for word in feature_set:
        docs_with_word=0
        for w_list in word_array:
            if word in w_list:
                docs_with_word+=1
        idf_num=math.log(len(f_names)/docs_with_word)
        idf_list.append(idf_num)
    
    return idf_list
def main():
    file_names=gen_names()
    base_feature_set=build_base_feature_set(file_names)
    print("Base feature set created!")
    #feature_set=base_feature_set
    #change the following functions to change the type of preprocessing
    #-------------------------------------------------------------------------------------
    feature_set=remove_stop_word('stopwords_3.txt', base_feature_set)
    feature_set=random_feature_select(feature_set, 1000)
    idf_list=idf(file_names, feature_set)
    #-------------------------------------------------------------------------------------
    print("Preprocessing performed")
    num=input("Enter data number: ")
    
    feature_set_stats(feature_set,num)
    create_dataset(file_names, feature_set,num,idf_list)
    print("dataset created Done!")
     
#test()   
main()
#print(gen_names())
#print(string.punctuation)
