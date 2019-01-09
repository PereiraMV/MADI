# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 15:45:48 2018

@author: Marc
"""
import transition as ts
import state as st
import grille as gr
import random
class PDM:
	grille=None
	listState=dict()
	listTrans=dict()
	#a key of the dict is ((i,j),sword,key,tresor,type)
	#type=0 decision node , type=1 natural node
	playerPos=list()
	


	def __init__(self,grille):
		self.grille=grille
		self.playerPos=(grille.size[0]-1,grille.size[1]-1)
		#CREATE THE STATES
		self.grille=grille
		for i in range(grille.size[0]):
			for j in range(grille.size[1]):
				for sword in range (2):
					for tresor in range (2):
						for key in range (2):
							if grille.tab[i][j]!='M' and grille.tab[i][j]!='P' and grille.tab[i][j]!='W' and grille.tab[i][j]!='C':
								self.listState[((i,j),sword,key,tresor,0)]=st.state(sword,tresor,key,(i,j),0,grille)
							if grille.tab[i][j]!='W':
								self.listState[((i,j),sword,key,tresor,1)]=st.state(sword,tresor,key,(i,j),1,grille)
		self.listState[((-1,-1),-1,-1,-1,1)]=st.state(-1,-1,-1,(-1,-1),1,grille,param="fail")
		
		self.listState[((-2,-2),-2,-2,-2,1)]=st.state(-2,-2,-2,(-2,-2),1,grille,param="sucess")
		
		self.listState[((-1,-1),-1,-1,-1,2)]=st.state(type=2,param="fail")
		self.listState[((-2,-2),-2,-2,-2,2)]=st.state(type=2,param="sucess")

		self.listTrans[((-1,-1),-1,-1,-1,1)]=[ts.transition(self.grille,self.listState[((-1,-1),-1,-1,-1,1)],[self.listState[((-1,-1),-1,-1,-1,2)]],[1],-3000)]
		self.listTrans[((-2,-2),-2,-2,-2,1)]=[ts.transition(self.grille,self.listState[((-2,-2),-2,-2,-2,2)],[self.listState[((-2,-2),-2,-2,-2,2)]],[1],-3000)]
		self.listTrans[((-1,-1),-1,-1,-1,2)]=[]
		self.listTrans[((-2,-2),-2,-2,-2,2)]=[]
		#create the transitions
		for i in range(grille.size[0]):
			for j in range(grille.size[1]):
				for sword in range (2):
					for tresor in range (2):
						for key in range (2):
							if grille.tab[i][j]!='M' and grille.tab[i][j]!='P' and grille.tab[i][j]!='W' and grille.tab[i][j]!='C':
								stateCurrent=self.listState[((i,j),sword,key,tresor,0)]
								#state where the player cannot move(don't have a choice) or go in
								self.listTrans[((i,j),sword,key,tresor,0)]=ts.transitionDecision(stateCurrent,self.listState,grille)
							if grille.tab[i][j]!='W':
								stateCurrent=self.listState[((i,j),sword,key,tresor,1)]
								self.listTrans[((i,j),sword,key,tresor,1)]=ts.action(stateCurrent,self.listState,grille)
								
		return
		
		
		
		
		

	def play(self):
		
		statePlayer=self.listState[(self.playerPos,0,0,0,0)]
		print "player key "+str(statePlayer.key)+" player tresor "+str(statePlayer.tresor)+" player sword "+str(statePlayer.sword) 
		while (True):
			self.grille.affichage(self.playerPos)
		
			if statePlayer.type==0:
				pc=-1
				
				while(pc==-1):
					print "Choose between z=go top,q=go left,s=go down,d=go right"
					playerMove=raw_input()
					
					if (playerMove=='z'):
						if self.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.tresor,0)][0]!=None:
							pc=0
					if (playerMove=='s'):
						if self.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.tresor,0)][1]!=None:
							pc=1
					if (playerMove=='q'):
						if self.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.tresor,0)][2]!=None:
							pc=2
					if (playerMove=='d'):
						if self.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.tresor,0)][3]!=None:
							pc=3

				statePlayer=self.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.tresor,0)][pc].listState[0]
				self.playerPos=statePlayer.position
				
			if statePlayer.type==1:
			



				transPlayer=self.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.tresor,1)][0]
				proba=transPlayer.listProba
				states=transPlayer.listState
				nb=random.random()
				sumi=0
				indice=-1
				for i in range(len(proba)):
					sumi=sumi+proba[i]
					if nb<=sumi:
						indice=i
						break
				statePlayer=states[indice]
				self.playerPos=statePlayer.position
				
			if statePlayer.type==2:
				
				if statePlayer.stateType=="fail":
					print "you failed"
					break
				if statePlayer.stateType=="sucess":
					print "you win"
					break
			print "player key "+str(statePlayer.key)+" player tresor "+str(statePlayer.tresor)+" player sword "+str(statePlayer.sword) 
				


						
					

			
		


	

if __name__ == "__main__":
	grilleA=gr.grille("exemple2.txt")
	#grilleA.affichage((0,0))
	pdm=PDM(grilleA)
	#print(pdm.listState)
	#print(grilleA.size,grilleA.tab)
	
	pdm.play()

