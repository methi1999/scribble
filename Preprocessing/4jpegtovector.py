import pickle
import PIL 
from PIL import Image
import numpy as np
import os

# for letter in ['o','p','q','r','s','u']:
for letter in ['a','b','c','e','g']:
	samples = len([f for f in os.listdir('./Letters/'+letter+'/') if f[-5:] == ".jpeg"])
	databasename='./Letters/'+letter+'/'+letter+'_vector.p'
	database=[]
	for i in range(0,samples):
		imagename='./Letters/'+letter+'/img_'+letter+'_'+str(i)
		img = Image.open(imagename+'.jpeg')
		#To create vector:
		img = img.convert('L')
		dat=np.array(img)/255
		database.append(dat)
	pickle.dump(database,open(databasename,'wb'))
	print("Exported vector for letter " + letter)
		