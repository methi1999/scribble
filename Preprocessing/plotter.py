import matplotlib.pyplot as plt
import pickle

letter='g'
data=pickle.load(open('./Letters/'+letter+'/'+letter+'_final_bounded.p','rb'))
# print(len(data))
# print(type(data[0][0]))
for letter in data[:20]:
	x=[p[0] for p in letter]
	y=[p[1] for p in letter]
	# print(x,y)
	plt.xlim((0,max(x)+10))
	plt.ylim((0,max(y)+10))
	plt.plot(x,y)
	plt.show()