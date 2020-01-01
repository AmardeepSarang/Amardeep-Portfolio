
'''
Created on 2019 M03 18
@author: Anthony
'''
# from matplotlib import pyplot
# from nltk.stem.porter import *

import pickle

from sklearn import cluster
from sklearn.decomposition import PCA

import numpy as np
import pandas as pd

vectors_file = open('yeet.pkl', 'rb')

results = pickle.load(vectors_file)

vectors_file.close()

results = np.array(results)


pca = PCA(3)
pca.fit(results)
pca_data = pd.DataFrame(pca.transform(results))
print("PCA HEAD DATA")
print(pca_data.head())

dbscan = cluster.DBSCAN(eps=5, min_samples=1).fit(results) # if you get new tweets and run from a new model #1

#dbscan_file = open('clusters_db.pkl', 'rb') # if you have a model and don't need to train it again #2
#dbscan = pickle.load(dbscan_file) # if you have a model and don't need to train it again #2
#dbscan_file.close() # if you have a model and don't need to train it again #2

count = 1
print(dbscan.labels_)
for label in dbscan.labels_:
    #if (label == 1):
    print(count, label) # label is the cluster they're in
    
    count += 1

dbscan_file = open('clusters.pkl', 'wb') # if you get new tweets and run from a new model #1
pickle.dump(dbscan, dbscan_file) # if you get new tweets and run from a new model #1
dbscan_file.close() # if you get new tweets and run from a new model #1

