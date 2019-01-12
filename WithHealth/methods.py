from PDM import *

import numpy as np
import time 
from gurobipy import *
import random
import matplotlib as mpl
import matplotlib.pyplot as plt


def timer(f):#decorateur pour timer du temps que prend le picross a s executer
    def wrapper(*args):
        t0=time.time()
        res=f(*args)
        t='%.2f' % (time.time()-t0)
        print("Temps d'execution : ",t," secondes")
        return res
    return wrapper

def iteration_value(pdm,gam,eps=0.000001):
	cpt=0
	
	for key,state in pdm.listState.items():
		state.reset()
	while True:
		for key,state in pdm.listState.items():
			#transState list of transition
			transState=pdm.listTrans[key]
			if len(transState)==0:
				continue
			Q=[]
			for trans in transState:
				if trans==None:
					Q.append(None)
					continue
				proba=trans.listProba
				states=trans.listState
				reward=trans.reward
				Q.append(reward)
				for i in range (len(states)):
					Q[-1]+=1.0*gam*proba[i]*states[i].vpast
			state.optimal=np.argmax(Q)
			state.vnext=Q[state.optimal]
		allEq=True
		somme=[]
		for key,state in pdm.listState.items():
			somme.append(abs(state.vnext-state.vpast))
			if not(state.compare()):
				allEq=False
			state.update()
		cpt+=1	
#		print cpt,np.max(somme)
		if allEq or np.max(somme)<eps:
			break
			
#	print("compteur "+str(cpt))
#	for i in range(pdm.grille.size[0]):
#			for j in range(pdm.grille.size[1]):
#				if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W':
#					#position sword key tresor type
#					print pdm.listState[((i,j),0,1,1,1,0)].optimal,
#				else:
#					print 4,
#			print
#	affichage_of_play(pdm,((0,0),0,1,1,1,0))
#	affichage_policy(pdm)

	return

def optimal_Pl(pdm,gam,model_name="PDM"):
	m=Model(model_name)
	for key,state in pdm.listState.items():
		state.reset()

	#create variables
	for key,state in pdm.listState.items():
		if state.type==2:
			state.variablePL=m.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=0)
		else:
			state.variablePL=m.addVar(vtype=GRB.CONTINUOUS,lb=-GRB.INFINITY)
		m.update()
	
	#create objective
	obj = LinExpr();
	obj =0
	obj = quicksum([state.variablePL for key,state in pdm.listState.items() ])
	m.setObjective(obj,GRB.MINIMIZE)
	
	#create constraints
	for key,state in pdm.listState.items():
		#transState list of transition
		transState=pdm.listTrans[key]
		if len(transState)==0:
			continue
		for trans in transState:
			if trans==None:
				continue
			Q=[]
			proba=trans.listProba
			states=trans.listState
			reward=trans.reward
			Q.append(reward)
			#Q.append(-1.0*state.variablePL)
			for i in range (len(states)):
				Q.append(1.0*gam*proba[i]*states[i].variablePL)
			#print(state.stateType,state.type,state.position)
			print(Q)
			m.addConstr(state.variablePL>=quicksum(Q))
	m.write("output.lp")
	m.optimize()
	
	#######
	
	for key,state in pdm.listState.items():
		#transState list of transition
		transState=pdm.listTrans[key]
		if len(transState)==0:
			continue
		Q=[]
		for trans in transState:
			if trans==None:
				Q.append(None)
				continue
			proba=trans.listProba
			states=trans.listState
			reward=trans.reward
			Q.append(reward)
			for i in range (len(states)):
				Q[-1]+=1.0*gam*proba[i]*states[i].variablePL.x
		state.optimal=np.argmax(Q)
	
	
	####display
#	for i in range(pdm.grille.size[0]):
#		for j in range(pdm.grille.size[1]):
#			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' :
#				#position sword key tresor type
#				print pdm.listState[((i,j),0,1,1,0,0)].optimal,
#			else:
#				print 4,
#		print
#	affichage_of_play(pdm,((0,0),0,1,1,1,0))
#	affichage_policy(pdm)
	return 

def affichage_of_play(pdm,key,dual=False,ax=None,fig=None):#key= cle de listState
	toprint={0:"^",1:"v",2:"<",3:">",-1:"X"}
	toprint2=['g','r','m','y']
	print key
	if not(dual):
		fig, ax = plt.subplots()
	posPlayer,sword,key,health,tresor,typee=key
	if sword<0 or key<0 or health<0 or tresor<0:
		return
	typee=0
	print pdm.grille.size[0]
	for i in range(pdm.grille.size[0]):
		for j in range(pdm.grille.size[1]):
#			if i>1 or j>1:continue
			az=pdm.grille.tab[i][j]
#			print az
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' :
				#position sword key tresor type
				az=pdm.listState[((i,j),sword,key,health,tresor,typee)].optimal
#				print "kjlhkhjkhkh"
#				print pdm.grille.tab[i][j]
#				print az
				ax.scatter(j,pdm.grille.size[0]-i,marker=toprint[az],s=200,color=toprint2[az])
#				print pdm.listState[((i,j),sword,key,health,tresor,typee)].optimal,

			elif pdm.grille.tab[i][j]=='M':
				ax.scatter(j,pdm.grille.size[0]-i,marker="_",s=400,color="k")
			elif pdm.grille.tab[i][j]=='P':
				ax.scatter(j,pdm.grille.size[0]-i,marker="$O$",s=400,color="b")
			else:
				ax.scatter(j,pdm.grille.size[0]-i,marker="s",s=400,color="k")
#				print 4,
#		print
	plt.show()
	return
	
def affichage_policy(pdm,affichage=True):
	win=False
	toplay={0:"z",1:"s",2:"q",3:"d"}
	printer={'z':"Player goes top",'s':"Player goes down",'q':"Player goes left",'d':"Player goes Right"}
	print (pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,4,0,0
	statePlayer=pdm.listState[((pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,4,0,0)]
	if affichage:
		print "\nActual state"
		print "player key : "+str(statePlayer.key)+" player health : "+str(statePlayer.health)+" player tresor : "+str(statePlayer.tresor)+" player sword : "+str(statePlayer.sword) 
	while (True):
		if affichage:
			ax2=pdm.grille.affichage(pdm.playerPos,withpolicy=True)
			affichage_of_play(pdm,((0,0),statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,statePlayer.type),ax=ax2,dual=True)

		if statePlayer.type==0:
			pc=-1
			
			while(pc==-1):
				
#				playerMove=raw_input("press Enter to continue")
				playerMove=pdm.listState[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,statePlayer.type)].optimal
				if playerMove==-1: playerMove=0				
				playerMove=toplay[playerMove]
#				print pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,0)]
#				if affichage:
#					print printer[playerMove]
					
					
				if (playerMove=='z'):
					if pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,0)][0]!=None:
						pc=0
				if (playerMove=='s'):
					if pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,0)][1]!=None:
						pc=1
				if (playerMove=='q'):
					if pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,0)][2]!=None:
						pc=2
				if (playerMove=='d'):
					if pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,0)][3]!=None:
						pc=3

			statePlayer=pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,0)][pc].listState[0]
			pdm.playerPos=statePlayer.position
			
		if statePlayer.type==1:
		



			transPlayer=pdm.listTrans[(statePlayer.position,statePlayer.sword,statePlayer.key,statePlayer.health,statePlayer.tresor,1)][0]
			proba=transPlayer.listProba
			states=transPlayer.listState
			nb=random.random()
			sumi=0
			indice=-1
#				list_indice=[i for i in range(len(proba))]
			for i in range(len(proba)):
				sumi=sumi+proba[i]
				if nb<=sumi:
					indice=i
					break
#				indice=random.choice(list_indice,proba)
			
			statePlayer=states[indice]
			pdm.playerPos=statePlayer.position
			
		if statePlayer.type==2:
			
			if statePlayer.stateType=="fail":
				print "you failed"
				win=False
				break
			if statePlayer.stateType=="sucess":
				print "you win"
				win=True
				break
		if statePlayer.type!=2 and affichage:
			print "\nActual state"
			print "player key : "+str(statePlayer.key)+" player health : "+str(statePlayer.health)+" player tresor : "+str(statePlayer.tresor)+" player sword : "+str(statePlayer.sword)			


					

	return win

def next_state(Trans,indice,stateA):
	
	transPlayer=Trans[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,stateA.type)][indice]
	proba=transPlayer.listProba
	states=transPlayer.listState
	#print("position="+str(states[0].position))
	nb=random.random()
	#print "nb rand= "+str(nb)
	sumi=0
	indice2=-1
	#print(nb)
	#print(proba)
	for i in range(len(proba)):
		sumi=sumi+proba[i]
		if nb<=sumi:
			indice2=i
			break
#				indice=random.choice(list_indice,proba)
	#print("indice2   "+str(indice2))
	stateB=states[indice2]
	return (stateB,transPlayer.reward)



#((i,j),sword,key,health,tresor,1)
def Qlearning(pdm,gam,taux,timer,eps):
	Trans=pdm.listTrans.copy()
	for key,lisTrans in Trans.items():
		if key[5]==0:
			Trans[key]=[trans for trans in lisTrans if trans!=None]
			

	for key,state in pdm.listState.items():
		state.initiateQl(len(Trans[key]))
		state.reset()
	
	for i in range (0,timer):
		print("###############################################"+str(i))
		stateA=pdm.listState[((pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,4,0,0)]
		it=1
		epsilon=0.1
		while(stateA.type!=2):
			Qlstate=stateA.Ql
			indice=-1

			nb=random.random()
			#print("nb ="+str(nb))
			if (nb<epsilon):
				#print("hasard")
				indice=random.randint(0,len(Qlstate)-1)
			else:
				indice=np.argmax(Qlstate);

					
			#print("indice="+str(indice))
			stateB,reward=next_state(Trans,indice,stateA)
			
			maxB=0
			if (stateB.type!=2):
				maxB=np.max(stateB.Ql)
			#print("avant="+str(stateA.Ql))
			#print("crrrentstate="+str(stateA.position))
			new=stateA.Ql[indice]+taux(it)*(reward+(gam*maxB)-stateA.Ql[indice])
			stateA.Ql[indice]=new
			#print("new="+str(new))
			#print("apres="+str(stateA.Ql))
			#print(reward)
		
			#print(stateB.position)

			stateA=stateB
			it+=1
			#update of epsilon
			if (epsilon<=eps):
				epsilon=eps
			else:
				epsilon=epsilon-0.0001
			
		
		
		####display and put in optimal
	for i in range(pdm.grille.size[0]):
		for j in range(pdm.grille.size[1]):
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W':
				#position sword key health tresor type
				statecurr=pdm.listState[((i,j),0,0,4,0,0)]
				positionCurr=statecurr.position
				maxi=np.argmax(statecurr.Ql)
				stateNeig=Trans[((i,j),0,0,4,0,0)][maxi].listState[0]
				positionNeig=stateNeig.position

				if positionNeig[0]==positionCurr[0]-1 and positionNeig[1]==positionCurr[1]:
					print "0",
					statecurr.optimal=0
				if positionNeig[0]==positionCurr[0]+1 and positionNeig[1]==positionCurr[1]:
					print "1",
					statecurr.optimal=1
				if positionNeig[0]==positionCurr[0] and positionNeig[1]==positionCurr[1]-1:
					print "2",
					statecurr.optimal=2
				if positionNeig[0]==positionCurr[0] and positionNeig[1]==positionCurr[1]+1:
					print "3",
					statecurr.optimal=3
#			else:
#				print "4",
#				statecurr.optimal=4
		print
		
#	pdm.grille.affichage((0,0))
		
	return
	
def affichage_one_state_policy(pdm,key=0,health=4,tresor=0,sword=0):
	sword,key,health,tresor
	key=((0,0),sword,key,health,tresor,0)
	affichage_of_play(pdm,key)
	
if __name__ == "__main__":
	#generate grille
	grilleA=gr.grille("grille.txt")
	grilleA.generate_solvable(4,4,.3,.2,.1,1,1,3,nb_try=500)
	#grilleA.affichage((grilleA.size[0]-1,grilleA.size[0]-1))

	#Solve
	pdm=PDM(grilleA)
	
#	iteration_value(pdm,0.99)
#	optimal_Pl(pdm,0.99)
	Qlearning(pdm,0.99,lambda x:1.0/x,10000,eps=0.05)
	
	#affichage
	affichage_policy(pdm)
#	affichage_one_state_policy(pdm,key=0,health=4,tresor=0,sword=0)
	
	




