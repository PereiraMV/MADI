# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

import time
def timer(f):
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


	def affichage2(self,posPlayer):

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

	def affichage(self,posPlayer,withpolicy=False):
#		plt.subplot(1,2,1)
		change={'B':0,'W':1,'T':2,'E':3,'K':9,'R':5,'C':6,'S':7,'M':8,'P':4,'O':10}
		toprint=['T','E','R','C','K','S','M','P','O']
		color={'T':'y','E':'orange','K':'silver','R':'cyan','C':'magenta','S':'g','M':'k','P':'b','O':'y'}
		m=self.tab[:][:]
		print m
		new_m=[]
		for i in m:
			new_m.append(map(lambda x:change[x],i))
		m=new_m
		fig=None
		ax1=None
		ax2=None
		
		if not(withpolicy):
			fig, ax1 = plt.subplots()
		else:
			fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12, 5))
		m[posPlayer[0]][posPlayer[1]]=11
		cmap=mpl.colors.ListedColormap(['w', 'k','w'])
		bounds = np.array([0, 0.1, 1.1,2.1])
		norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

		ax1.scatter(posPlayer[1],posPlayer[0],marker='o',color='red',s=500)
		for i in range(len(self.tab)):
			for j in range(len(self.tab)):
				az=self.tab[i][j]
				if az in toprint:
					c=color[az]
					az='$'+az+'$'
					if az=='$M$' : az='_'
					ax1.scatter(j,i,marker=az,color=c,s=200)
		
		
#		plt.imshow(m,cmap=cmap,norm=norm,interpolation="none")
		ax1.imshow(m,cmap=cmap,norm=norm,interpolation="none")
		if not(withpolicy):
			plt.show()
		return ax2
		
	def generate_solvable(self,nb_line,nb_col,pw,po,pc,max_key,max_sword,max_portal,nb_try=30):
		if nb_line<4 or nb_col<4:
			print "Dimentions trop petites"
			return False
		self.generate(nb_line,nb_col,pw,po,pc,max_key,max_sword,max_portal)
		sucess=self.is_solvable()
		while (not(sucess) and nb_try>0):
			self.generate(nb_line,nb_col,pw,po,pc,max_key,max_sword,max_portal)
			sucess=self.is_solvable()
			nb_try-=1
			print nb_try
		if nb_try<=0:
			print "Fail generating"
			return False
		else:
			print "Generation succeed"
			return True
			
		
		return
	def generate(self, nb_line, nb_col, pw, po, pc, max_key, max_sword, max_portal):
		#nbline,nbcol,propotion_wall,proportion_obstacles ,proportion_crack,nombre_key,nombre_max_sword,nombre_max_portal
	#Obstacle=Ennemy or Traps "E" or "R"
		self.size = (nb_line,nb_col)
		self.tab = []
		for i in range(nb_line):
			self.tab.append(['B'] * nb_col)
		for i in range(nb_line):
			for j in range(nb_col):
				if random.uniform(0, 1) < pw:
					self.tab[i][j] = 'W'
				elif random.uniform(0, 1) < po:
					#ennemy
					if random.randint(0, 1) == 0:
						self.tab[i][j] = 'E'
					else:
						self.tab[i][j] = 'R'
				elif random.uniform(0, 1) < pc:
					self.tab[i][j] = 'C'
		#sword
		for key in range(max_sword):
			self.tab[random.randint(0, nb_line-1)][random.randint(0, nb_col-1)] = 'S'
			
		#portals
		for key in range(max_portal):
			self.tab[random.randint(0, nb_line-1)][random.randint(0, nb_col-1)] = 'P'
		
		#keys
		for key in range(max_key):
			self.tab[random.randint(0, nb_line-1)][random.randint(0, nb_col-1)] = 'K'
		#tresor
		self.tab[0][0] = 'T'
		#starting point
		self.tab[nb_line - 1][nb_col - 1] = 'O'


	def export(self,filename="exemple.txt"):
		with open(filename,"w") as f:
			f.write(str(self.size[0])+" "+str(self.size[1])+"\n")
			for i in range(len(self.tab)):
				string=""
				for j in range(len(self.tab[i])):
					string+=self.tab[i][j]
					if j!=len(self.tab[i])-1:
						string+=" "
				f.write(string+"\n")
		return
		
	def is_solvable(self):
		if self.tab:
			if not self.has_key():
				return False
			if not self.way_possible("K"):
				return False
			if not self.way_possible("T"):
				return False
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				if not(self.way_possible('Z',i,j)):
					return False
		return True

	def has_key(self):
		for row in self.tab:
			for cell in row:
				if cell == "K":
					return True
		return False
		
	def way_possible(self,objective,indice_i=-1,indice_j=-1):
		Q = []
		visited = []
		Q.append([self.size[0] - 1, self.size[1] - 1])
		visited.append([self.size[0] - 1, self.size[1] - 1])  # start is visited
		while len(Q) > 0:
			node = Q.pop()
			neighbours = [[node[0] - 1, node[1]], [node[0] + 1, node[1]], [node[0], node[1] - 1],[node[0], node[1] + 1]]
			for n in neighbours:
				if 0 <= n[0] < self.size[0] and 0 <= n[1] < self.size[1]:
					if self.tab[n[0]][n[1]] == objective or (n[0],n[1])==(indice_i,indice_j):
						return True
					else:
						if self.tab[n[0]][n[1]] != "W" and self.tab[n[0]][n[1]] != "C":
							if n not in visited:
								Q.append(n)
								visited.append(n)
		return False
		

if __name__ == "__main__":
    
	grilleA=grille("exemple2.txt")
	#print(grilleA.checkCell((0,0)))
#	print(grilleA.size,grilleA.tab)
#	grilleA.affichage((0,0))
	grilleA.generate_solvable(16,16,.3,.2,.1,1,1,3,nb_try=500)
#	grilleA.is_solvable()
	grilleA.affichage((15,15))