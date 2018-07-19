"""
ITSP 2018
Scribble by Four-Play

An auxillary program which reads saved data, plots images and makes predictions

"""

# import the necessary packages
import numpy as np
import pickle
import scipy.ndimage as ireader
import os
import matplotlib.pyplot as plt
import PIL 
from PIL import Image

#This function reads the raw (x,y) values of the keystrokes and plots it using matplotlib. This figure is then dumped saved as a jpeg
def ptoj(num,nstrokes):
	
	#Read data
	x,y,eg=[],[],[]
	for i in range(nstrokes):
		eg.append(pickle.load(open('../Vectors/boundedVec_'+str(num)+'_'+str(i)+'.p','rb')))

	#Flip the data laterally since webcam detects it in an inverted orientation
	for i in range(len(eg)):	
		x.append([-p[0] for p in eg[i]])
		y.append([-p[1] for p in eg[i]])

		#Apply low-pass filter to reduce high-frequency noise. An average of the surrounding (x,y) values is calculated

		if len(x[i])>20:
			for j in range(10,len(x[i])-10):
				x[i][j]=sum(x[i][j-10:j+11])/21.0
		if len(y[i])>20:
			for j in range(10,len(y[i])-10):
				y[i][j]=sum(y[i][j-10:j+11])/21.0

	#Plot all the strokes on the same graph. The letters i,j,f,t have nstrokes=2, rest have nstrokes=1
	for i in range(nstrokes):
		#Specify graph parameters
		plt.axis('off')
		plt.gca().set_aspect('equal', adjustable='box')
		plt.plot(x[i],y[i],c='black',linewidth=5)

	#Save jpeg
	imagename='../Images/img_'+str(num)+'.jpeg'
	plt.savefig(imagename,bbox_inches='tight')
	plt.gcf().clear()

	#Resize and save again. plt.savefig takes size arguments in terms of dps and not pixels. Since there is no standard convertion for dps->pixel, we open, resize and save the image again
	#Since our dataset is also 28x28
	basewidth = 28
	baseheight = 28
	img = Image.open(imagename)
	img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
	img.save(imagename)

	#Dump a nparray with each element containing the scaled pixel intensities
	img = img.convert('L')
	dat=np.array(img)/255
	pickle.dump(dat,open('../Images/nparray_'+str(num)+'.p','wb'))

#Predict the letter by feeding it to the model
def predict(num,model):

	im=pickle.load(open('../Images/nparray_'+str(num)+'.p','rb'))
	
	#Convention for feeding data to a Keras for model
	im=im.reshape((1,28,28,1))
	probs=model.predict(im)
	prediction = probs.argmax(axis=1)
	
	#ASCII value of 'a' is 97
	character=chr(97+prediction)
	print(character)
	return character