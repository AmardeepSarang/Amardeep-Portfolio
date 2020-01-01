import pickle

from collections import Counter
import numpy as np
import pandas as pd
import string
from textblob import TextBlob

def cluster_eval(words_in_cul):

	c = Counter(words_in_cul)
	top_ten=c.most_common(10)
	print(top_ten)


kmeans_file = open('clusters.pkl', 'rb') # if you have a model and don't need to train it again #2
kmeans = pickle.load(kmeans_file) # if you have a model and don't need to train it again #2
kmeans_file.close() # if you have a model and don't need to train it again #2


tweet_file=open("all_tweets.csv","r")
tweets=[]
for line in tweet_file:
	table = str.maketrans({key: None for key in string.punctuation})
	line=line.strip()
	line=line.translate(table)
	line=line.replace("'","")
	text=TextBlob(line)
	tweets.append(text.noun_phrases)

NUM_CLUSTER=25
count = 1
for l in range(1,NUM_CLUSTER):
	words_in_cul=[]
	for label in kmeans.labels_:
	    if (label == l):
	    	for word in tweets[count-1]:
	    		if(word not in words_in_cul):
	    			words_in_cul.append(word)

	    	count += 1
	print("The top ten words in cluster: "+str(l))
	cluster_eval(words_in_cul)
	    

