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

def iteration_value(pdm,gam):
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
		for key,state in pdm.listState.items():
			if not(state.compare()):
				allEq=False
			state.update()
		cpt+=1	
		print(cpt)
		if allEq:
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
	affichage_of_play(pdm,((0,0),0,1,1,1,0))

	return
@timer
def optimal_Pl(pdm,gam):
	m=Model("PDM")
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
			#print(Q)
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
	for i in range(pdm.grille.size[0]):
		for j in range(pdm.grille.size[1]):
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' :
				#position sword key tresor type
				print pdm.listState[((i,j),0,1,0,0,0)].optimal,
			else:
				print 4,
		print
	return 

def affichage_of_play(pdm,key):#key= cle de listState
#	print pdm.listState
	toprint={0:"^",1:"v",2:"<",3:">"}
	fig, ax = plt.subplots()
	posPlayer,sword,key,health,tresor,typee=key
	for i in range(pdm.grille.size[0]):
		for j in range(pdm.grille.size[1]):
#			if i>1 or j>1:continue
			az=pdm.grille.tab[i][j]
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' :
				#position sword key tresor type
				az=pdm.listState[((i,j),sword,key,health,tresor,typee)].optimal
				ax.scatter(j,pdm.grille.size[0]-i,marker=toprint[az],s=200)
				print pdm.listState[((i,j),sword,key,health,tresor,typee)].optimal,
			elif pdm.grille.tab[i][j]=='M':
				ax.scatter(j,pdm.grille.size[0]-i,marker="_",s=400,color="k")
			elif pdm.grille.tab[i][j]=='P':
				ax.scatter(j,pdm.grille.size[0]-i,marker="$O$",s=400,color="b")
			else:
				ax.scatter(j,pdm.grille.size[0]-i,marker="s",s=400,color="k")
				print 4,
		print
	return
    
    
def next_state(pdm,indice,stateA):
	
	transPlayer=pdm.listTrans[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,stateA.type)][indice]
	
	proba=transPlayer.listProba
	states=transPlayer.listState
	nb=random.random()
	#print "nb rand= "+str(nb)
	sumi=0
	indice2=-1
	print(nb)
	print(proba)
	for i in range(len(proba)):
		sumi=sumi+proba[i]
		if nb<=sumi:
			indice2=i
			break
#				indice=random.choice(list_indice,proba)
	print("indice2   "+str(indice2))
	stateB=states[indice2]
	return (stateB,transPlayer.reward)

def my_min(l):
	toRet=[pdm.listTrans[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,stateA.type)][i] for i in range(l) if i!=None ]
	return np.argmin(toRet)
#((i,j),sword,key,health,tresor,1)
def Qlearning(pdm,gam,taux,timer):
	for key,state in pdm.listState.items():
		state.initiateQl(len(pdm.listTrans[key]))
	stateA=pdm.listState[((pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,4,0,0)]
	for i in range (1,timer):
		if (stateA.type==2):
			stateA=pdm.listState[((pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,4,0,0)]
		print i
		Qlstate=stateA.Ql
		start=False
		indice=-1
		print(Qlstate)
		if all([k==0 for k in Qlstate]):
			start=True
		if start==False:
			print "avant" 
			print (Qlstate)
			Qlstate=Qlstate+abs(np.min(Qlstate))
			Qlstate=Qlstate/np.sum(Qlstate)
			print Qlstate
			for k in range(len(Qlstate)):
				if pdm.listTrans[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,stateA.type)][k]==None:
					Qlstate[k]=0
			Qlstate/=np.sum(Qlstate)
	
				
			nb=random.random()
			sumi=0
			for j in range(len(Qlstate)):
				sumi=sumi+Qlstate[j]
				if nb<=sumi:
					indice=j
					break
			
		
		
		else:
			indice=random.randint(0,len(Qlstate)-1)
#			print "indice " + str(indice)
			while (pdm.listTrans[(stateA.position,stateA.sword,stateA.key,stateA.health,stateA.tresor,stateA.type)][indice]==None):
				indice=random.randint(0,len(Qlstate)-1)
		print("indice"+str(indice))
		stateB,reward=next_state(pdm,indice,stateA)
		maxB=0
		print(stateA.position)
		if (stateB.type!=2):
			maxB=np.max(stateB.Ql)

		stateA.Ql[indice]+=taux(i)*(reward+gam*(maxB-stateA.Ql[indice] ) )
		print("hello  ")
		print(stateA.Ql)
		stateA=stateB
		####display
	for i in range(pdm.grille.size[0]):
		for j in range(pdm.grille.size[1]):
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' :
				#position sword key tresor type
				print np.argmax(pdm.listState[((i,j),0,0,4,0,0)].Ql),
			else:
				print 4,
		print
		
	return

grilleA=gr.grille("exemple2.txt")
#grilleA.affichage((0,0))
pdm=PDM(grilleA)
iteration_value(pdm,0.6)
#optimal_Pl(pdm,0.99)
#Qlearning(pdm,0.99,lambda x:1.0/x,10000)




