import matplotlib.pyplot as plt
import pickle

# data=pickle.load(open('q3.p','rb'))
# del data[-2]
# pickle.dump(data,open('q3.p','wb'))
count=0
for i in range(1,7):
	data=pickle.load(open("q"+str(i)+".p",'rb'))
	count += len(data)
print(count)