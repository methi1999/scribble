import pickle
import numpy as np

data=[]
count=[]
chars=['o','p','q','r','s','a','b','c','e','g']

for letter in chars:
	namekey='./Letters/'+letter+'/'+letter+'_vector_normalized.p'
	curr=pickle.load(open(namekey,'rb'))
	for sample in curr:
		data.append(sample)
	count.append(len(curr))
# print(count)
data=np.array(data)
print(len(data))
# data=data.flatten()
# print(data)
pickle.dump((data,count),open('finaldata.p','wb'))