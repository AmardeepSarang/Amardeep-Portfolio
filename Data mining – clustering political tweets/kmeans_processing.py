'''
Created on 2019 M03 18

@author: Anthony
'''
# from matplotlib import pyplot
# from nltk.stem.porter import *
import math
import pickle

from matplotlib import colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from sklearn import cluster
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

vectors_file = open('yeet.pkl', 'rb')

results = pickle.load(vectors_file)

vectors_file.close()

results = np.array(results)

# import tkinter
# file = open("preprocessed_data/data_tf.csv", "rb")
# values = np.loadtxt(file, delimiter=",")
# x = list(values)
# result = np.array(x).astype("float")
# print("result numpy array")
# print(result)
# file.close()
# 
pca = PCA(3)
pca.fit(results)
pca_data = pd.DataFrame(pca.transform(results))
print("PCA HEAD DAT??")
print(pca_data.head())

kmeans = cluster.KMeans(n_clusters=25, random_state=0).fit(results) # 1

# kmeans_file = open('clusters.pkl', 'rb') #2
# kmeans = pickle.load(kmeans_file) #2
# kmeans_file.close() #2 

count = 1

for label in kmeans.labels_:
    if (label == 1):
        print(count, label)
    
    count += 1

kmeans_file = open('clusters.pkl', 'wb') # 1
pickle.dump(kmeans, kmeans_file) # 1   
kmeans_file.close() # 1

''' Generating different colors in ascending order  
                                of their hsv values '''
# colors = list(zip(*sorted((
#     tuple(mcolors.rgb_to_hsv(
#                           mcolors.to_rgba(color)[:3])), name)
#     for name, color in dict(
#     mcolors.BASE_COLORS, **mcolors.CSS4_COLORS
# ).items())))[1]
# 
# # number of steps to taken generate n(clusters) colors
# skips = math.floor(len(colors[5:-5]) / 4)
# cluster_colors = colors[5:-5: skips]
# 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(pca_data[0], pca_data[1], pca_data[2],
#            c=list(map(lambda label: cluster_colors[label],
#                       kmeans.labels_)))
# 
# str_labels = list(map(lambda label: '% s' % label, kmeans.labels_))
# 
# list(map(lambda data1, data2, data3, str_label:
#          ax.text(data1, data2, data3, s=str_label, size=3.5,
#                  zorder=30, color='k'), pca_data[0], pca_data[1],
#          pca_data[2], str_labels))
# 
# # plt.show()
# 
# # y_kmeans = kmeans.predict(result)
# # print("kmeans centers")
# # print(kmeans.cluster_centers_)
# 
# print("plot")
# 
# # plt.scatter(result[:, 0], result[:, 1], c=y_kmeans, cmap="viridis", label="True Position")
# # centers = kmeans.cluster_centers_
# # plt.scatter(centers[:, 0], centers[:, 1], c="black",
# #             s=200)
# plt.show()
