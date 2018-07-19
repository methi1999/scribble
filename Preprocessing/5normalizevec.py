import pickle
import numpy as np

for letter in ['a','b','c','e','g']:
# for letter in ['h','k']:
	databasename='./Letters/'+letter+'/'+letter+'_vector'
	data=pickle.load(open(databasename+'.p','rb'))
	# print(type(data[0]))
	for sample in data:
		sample -= sample.mean()
	pickle.dump(data,open(databasename+'_normalized.p','wb'))
	print("Exported normalized vector for letter " + letter)
		