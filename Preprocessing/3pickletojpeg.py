import matplotlib.pyplot as plt
import pickle
import PIL 
from PIL import Image
import numpy as np

# for letter in ['o','p','q','r','s','u']:
for letter in ['a','b','c','e','g']:
	source='./Letters/'+letter+'/'+letter+'_final_bounded.p'
	data=pickle.load(open(source,'rb'))
	# print(len(data))
	# print(type(data[0][0]))
	# dataname='./Letters/'+letter+'/'+letter+'_vector'
	# database=[]
	for i in range(0,len(data)):
		eg=data[i]
		x=[p[0] for p in eg]
		y=[p[1] for p in eg]

		plt.axis('off')
		plt.gca().set_aspect('equal', adjustable='box')
		plt.plot(x,y,c='black',linewidth=5)
		imagename='./Letters/'+letter+'/img_'+letter+'_'+str(i)
		plt.savefig(imagename+'.jpeg',bbox_inches='tight')
		plt.gcf().clear()

		basewidth = 28
		baseheight = 28
		img = Image.open(imagename+'.jpeg')
		img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
		#To save jpeg:
		img.save(imagename+'.jpeg')

		#To create vector:
		# img = img.convert('L')
		# dat=np.array(img)/255
		# database.append(dat)
	# pickle.dump(database,open(dataname,'wb'))
	print("Done with letter " + letter)
		