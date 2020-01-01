"""
-------------------------------------------------------
Q3.py
k nearest neighbor implementation with 10-fold testing
using  Wisconsin Breast Cancer Database (January 8, 1991)
-------------------------------------------------------
Author:  Amardeep Sarang
ID: 160112080
Email:  sara2080@mylaurier.ca
__updated__ = "2018-10-20"
-------------------------------------------------------
"""
import csv
import math
from _operator import itemgetter
from random import randint,choice

def load_data(file_name):
    #open file into 2x2 array
    dataset=[]
    f=open(file_name,"r")
    word_list=[]
    for line in f:
        word_list=line.split(",")
        dataset.append(word_list)
    f.close()
    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            dataset[i][j] = float(dataset[i][j])
    return dataset

def split_test(data,test_num):
    '''
    splits data depending on fold  number
    '''
    test_set=data[test_num]
    traning_set=data[:test_num]+data[test_num+1:]
    return test_set, traning_set

def print_2d(array):
    ''''
    for testing
    '''
    
    i=1
    for row in array:
        print(i,end=". ")
        i+=1
        for x in row:
            print(x,end=" - ")
        print()
    print()
    

def euclidean_distance(a,b,length):
    '''
    calculates euclidean distance
    '''
    dist=0
    for i in range(length-1):
        dist+=pow(a[i]-b[i], 2)
     #   print(b[i])
    return math.sqrt(dist)

def k_nn_prediction(prediction_subject,trainng_set,k):
    '''
    returns prediction for prediction subject
    prediction_subject - single row of test set
    trainng_set - entire traing set
    k - number of neighbors that vote
    '''
    dist_and_outcomes=[]
    
    
    #record distance and out come for each row of training set
    for train_row in trainng_set:
        dist_and_outcomes.append([euclidean_distance(prediction_subject, train_row,len(prediction_subject)),train_row[len(train_row)-1]])
    
    #sort by distance
    dist_and_outcomes=sorted(dist_and_outcomes, key=itemgetter(0))
    
    #get first k votes
    votes=[]
    for i in range(k):
        votes.append(dist_and_outcomes[i][1])
    
    return vote_count(votes)

def vote_count(votes):
    '''
    count votes and returns most voted
    '''
    counts=[0,0,0,0]
    key=[1,2,3,4]
    for v in votes:
        counts[int(v)-1]+=1
    max_i=0;
    max_v=counts[0]
    for i in range(len(counts)):
        if counts[i]>max_v:
            max_i=i
            max_v=counts[i]
    
    tie_votes=[]
    for i in range(len(counts)):
        if max_v==counts[i]:
            tie_votes.append(i)
    
    if len(tie_votes)==1:
        #no tie
        i=tie_votes[0]
        result=key[i]
    else:
        #tie, break at random
        i=choice(tie_votes)
    result=key[i]
    return result
    
def print_accuracy(accuracy_list,f_name):
    '''
    prints accuracy for each k value
    NOTE: it is printed in a format that turns it into csv
    '''
    
    print(f_name,end=',')
    for i in accuracy_list:
        print(round(i,3),end=",")
    print()
        
def gen_names():
    #generate file names
    f_names=[]
    for i in range(1,11):
        s='dataset_'+str(i)+'.txt'
        f_names.append(s)
    return f_names
        
def main():
    #load data
    f_names=gen_names()
   # f_names=['dataset_1.txt']
    print("K value",end=',')
    for i in [1,3,5,7,9]:
        print(i,end=",")
    print()
    for f_name in f_names:
        ab_table=load_data(f_name)
        
        accuracy_list=[]
        for k in [1,3,5,7,9]:
            tests_done=0
            tests_correct=0
            
            for fold in range(40):
            #spilt data
                test,train=split_test(ab_table, fold)
                
    
                result= k_nn_prediction(test, train, k)
                tests_done+=1
                #check if correct prediction was made
                #print("{}=={}".format(result,test[len(test)-1]))
                if result==test[len(test)-1]:
                    tests_correct+=1
                    
            accuracy=tests_correct/tests_done
            accuracy_list.append(accuracy)
            #print("A: {} C: {} D: {}".format(accuracy,tests_correct,tests_done))
        print_accuracy(accuracy_list,f_name)
    
def test():
    data=[1,2,3,4,5,6,7]
    
    for i in range(len(data)):
        test,train=split_test(data, i)
        print(test)
        print(train)
    
    
main()
#test()