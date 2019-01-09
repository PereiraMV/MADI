# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 15:46:45 2018

@author: Marc
"""
import grille as gr
import state as st

class transition:
	reward=0;
	stateA=None
	listState=list()
	listProba=list()
	#DM for decision maker because player has to choose in those transitions

	 
	def __init__(self,grille,stateA,statesB,proba,reward):
		self.stateA=stateA
		self.listState=statesB
		self.listProba=proba
		self.reward=reward
		

		
		return
		
def transitionDecision(stateA,listState,grille):
	listeNeigborType,nb=grille.checkNeigbors(stateA.position);
	transitions=[]
	for i in listeNeigborType:
		reward=-100
		statesB=[]
		if i==None:
			transitions.append(None)
			continue
		else:
			#((i,j),sword,key,tresor,type)
			statesB.append(listState[(i,stateA.sword,stateA.key,stateA.health,stateA.tresor,1)])
			transitions.append(transition(grille,stateA,statesB,[1],reward))
		
	
	return transitions
	
def action(stateA,listState,grille):
	reward=0
	statesB=[]
	transitions=[]
	if stateA.stateType=='M':
		listeNeigborType,nb=grille.checkNeigbors(stateA.position);
		transitions=[]
		#there will only be one transition
		for i in listeNeigborType:
			if i==None:
				continue
			else:
				#((i,j),sword,key,tresor,type)
				statesB.append(listState[(i,stateA.sword,stateA.key,stateA.health,stateA.tresor,1)])

		proba=[1.0/nb*1.0 for i in range (nb)]
		transitions.append(transition(grille,stateA,statesB,proba,reward))
		
		
	if stateA.stateType=='P':
		listPosition,nb=grille.checkCell(stateA.position)
		proba=[1.0/nb*1.0 for i in range(nb)]
		for i in listPosition:
			statesB.append(listState[(i,stateA.sword,stateA.key,stateA.health,stateA.tresor,1)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	if stateA.stateType=='K':
		proba=[1]
		if stateA.key==0:
			reward=1000
			statesB.append(listState[(stateA.position,stateA.sword,1,stateA.health,stateA.tresor,0)])
			
		else:
			reward=0
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))
		

	if stateA.stateType=='S':
		proba=[1]
		if stateA.sword==1 :
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
			
		else:
			statesB.append(listState[(stateA.position,1,stateA.key,stateA.health,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	if stateA.stateType=='T':
		proba=[1]
		if stateA.key==1 and stateA.tresor==0 :
			reward=1000
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,1,0)])
			
		else:
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	if stateA.stateType=='C':
		proba=[1]
		if stateA.health<2:
			statesB.append(listState[((-1,-1),-1,-1,-1,-1,1)])
		else:
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health-1,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))
		
	if stateA.stateType=='R':
		proba=[0.1,0.3,0.6]
		# death , teleport begining , nothing
		if stateA.health<2:
			statesB.append(listState[((-1,-1),-1,-1,-1,-1,1)])
		else:
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health-1,stateA.tresor,0)])
		statesB.append(listState[((grille.size[0]-1,grille.size[1]-1),stateA.sword,stateA.key,stateA.health,stateA.tresor,1)])
		statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	if stateA.stateType=='E':
		if stateA.sword==1 :
			proba=[1]
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		else:
			proba=[0.3,0.7]
			if stateA.health<2:
				statesB.append(listState[((-1,-1),-1,-1,-1,-1,1)])
			else:
				statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health-1,stateA.tresor,0)])
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	if stateA.stateType=='B':
		statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		proba=[1]
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	if stateA.stateType=='O':
		proba=[1]
		if stateA.key==1 and stateA.tresor==1:
			reward=10000
			statesB.append(listState[((-2,-2),-2,-2,-2,-2,1)])
			
		else:
			statesB.append(listState[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,0)])
		transitions.append(transition(grille,stateA,statesB,proba,reward))

	return transitions





