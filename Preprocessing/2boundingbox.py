import pickle
import matplotlib.pyplot as plt

final=[]
alphabet="g"
blmargin=20
noofbatches=3
letterdirectory='./Letters/'+alphabet+'/'
for i in range(1,noofbatches+1):
	batch=pickle.load(open(letterdirectory+alphabet+str(i)+'.p','rb'))
	for letter in batch:
		minx,miny,maxx,maxy=2000,2000,-2000,-2000
		for stroke in letter:
			if stroke[0]>maxx:
				maxx=stroke[0]
			elif stroke[0]<minx:
				minx=stroke[0]

			if stroke[1]>maxy:
				maxy=stroke[1]
			elif stroke[1]<miny:
				miny=stroke[1]
		current=[]
		# print(maxx,maxy,minx,miny)
		# minx,miny=2000,2000
		# for stroke in letter:
		# 	if stroke[0]<minx:
		# 		minx=stroke[0]
		# 	if stroke[1]<miny:
		# 		miny=stroke[1]	
		# print("X,Y seedha values:")
		x,y=0,0			
		for stroke in letter:
			xulta = stroke[0] - minx
			yulta = stroke[1] - miny
			# xseedha = stroke[0]-maxx+minx+blmargin
			# yseedha = stroke[1]-maxy+miny+blmargin
			xseedha = maxx-stroke[0]+20
			yseedha = maxy-stroke[1]+20
			# print(xseedha,yseedha)
			current.append((xseedha,yseedha))

		final.append(current)

pickle.dump(final,open(letterdirectory+alphabet+'_final_bounded.p','wb'))
print("Done with alphabet " + alphabet)
