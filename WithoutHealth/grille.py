# -*- coding: utf-8 -*-
"""

"""

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




if __name__ == "__main__":
    
	grilleA=grille("exemple2.txt")
	#print(grilleA.checkCell((0,0)))
	print(grilleA.size,grilleA.tab)
	grilleA.affichage((0,0))
