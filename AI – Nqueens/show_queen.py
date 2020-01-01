'''
Requires numpy and openCV to run, use pip to install
To run type python show_queens.py [N] [path to input file]
'''
import cv2
import numpy as np
import sys

f=open(sys.argv[2])
n=int(sys.argv[1])

img = np.zeros([n,n,3])
black=(0,0,0)
white=(255,255,255)
red=(0,0,255)
col=0
#create checker board
for i in range(n):

	for j in range(n):
		#print(col%2==0)
		if col%2==0:
			img[i][j]=white
		else:
			img[i][j]=black
		col+=1
	col+=1
#color queen cord red
for line in f:
	l=line.strip().split()
	x=int(l[4])-1
	y=int(l[9])-1
	img[x][y]=red

img=rescaled = cv2.resize(img, (700, 700), interpolation=cv2.INTER_AREA)

cv2.imwrite(str(n)+".jpg",img)
cv2.imshow(str(n), img)
cv2.waitKey(0)