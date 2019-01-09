# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import time
def timer(f):#décorateur pour timer du temps que prend le picross à s'executer
    def wrapper(*args):
        t0=time.time()
        res=f(*args)
        t='%.2f' % (time.time()-t0)
        print("Temps d'execution : ",t," secondes")
        return res
    return wrapper


class grille:
	size=list()
	tab=list()


	def __init__(self,filename):
		f= open(filename,'r')
		data=f.read().split("\n")
		size=data[0].split(" ")
		self.size=(int(size[0]),int(size[1]))
		for line in data[1:]:
			split=line.split(" ")
			self.tab.append(split)
			#self.tab[-1][-1]=split[-1][0]
		f.close()
		return

	def checkCell(self,position):
		listPosition=[]
		cpt=0
		for i in range (self.size[0]):
			for j in range (self.size[1]):
				if self.tab[i][j]!='W':
					cpt+=1
					listPosition.append((i,j))
					
		return listPosition,cpt

	def checkState(self,position):
		if (position[0]<0 or position[1]<0 or position[0]>=self.size[0] or position[1]>=self.size[1]):
			return False
		return True

	def checkNeigbors(self,position):
		listState=[]
		nb=0
		top=(position[0]-1,position[1])
		if self.checkState(top) and self.tab[top[0]][top[1]]!='W':
			nb+=1
			listState.append(top)
		else:
			listState.append(None)
		down=(position[0]+1,position[1])
		if self.checkState(down) and self.tab[down[0]][down[1]]!='W':
			nb+=1
			listState.append(down)
		else:
			listState.append(None)
		left=(position[0],position[1]-1)
		if self.checkState(left) and self.tab[left[0]][left[1]]!='W':
			nb+=1
			listState.append(left)
		else:
			listState.append(None)
		right=(position[0],position[1]+1)
		if self.checkState(right) and self.tab[right[0]][right[1]]!='W':
			nb+=1
			listState.append(right)
		else:
			listState.append(None)
		return listState,nb


	def affichage(self,posPlayer):

		for i in range (self.size[0]):
			for j in range (self.size[1]):

				

				if (i,j)==posPlayer:
					print 'J',
				else:
					print self.tab[i][j],

			print 
		if len(posPlayer)!=0:
			print 'Player on case '+self.tab[posPlayer[0]][posPlayer[1]]
					
		return 

	def affichage2(self,posPlayer):
		change={'B':0,'W':1,'T':2,'E':3,'K':9,'R':5,'C':6,'S':7,'M':8,'P':4,'O':10}
		toprint=['T','E','R','C','K','S','M','P','O']
		m=self.tab[:][:]
		new_m=[]
		for i in m:
			new_m.append(map(lambda x:change[x],i))
		m=new_m
				
		fig, ax = plt.subplots()
		m[posPlayer[0]][posPlayer[1]]=11
		cmap=mpl.colors.ListedColormap(['w', 'k','w'])
		bounds = np.array([0, 0.1, 1.1,2.1])
		norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

		ax.scatter(posPlayer[1],posPlayer[0],marker='o',color='red',s=500)
		for i in range(len(self.tab)):
			for j in range(len(self.tab)):
				az=self.tab[i][j]
				if az in toprint:
					az='$'+az+'$'
					if az=='$M$' : az='_'
					ax.scatter(j,i,marker=az,s=200)
		print posPlayer
		
		plt.imshow(m,cmap=cmap,norm=norm,interpolation="none")
		plt.show()
		
	


if __name__ == "__main__":
    
	grilleA=grille("exemple2.txt")
	#print(grilleA.checkCell((0,0)))
#	print(grilleA.size,grilleA.tab)
	grilleA.affichage2((0,0))
