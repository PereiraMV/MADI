from PDM import *

import numpy as np
import time 
from gurobipy import *


def timer(f):#décorateur pour timer du temps que prend le picross à s'executer
    def wrapper(*args):
        t0=time.time()
        res=f(*args)
        t='%.2f' % (time.time()-t0)
        print("Temps d'execution : ",t," secondes")
        return res
    return wrapper

@timer
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
		
		if allEq:
			break
			
	print("compteur "+str(cpt))
	for i in range(pdm.grille.size[0]):
			for j in range(pdm.grille.size[1]):
				if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' and pdm.grille.tab[i][j]!='C':
					#position sword key tresor type
					print pdm.listState[((i,j),0,1,1,0)].optimal,
				else:
					print 4,
			print

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
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' and pdm.grille.tab[i][j]!='C':
				#position sword key tresor type
				print pdm.listState[((i,j),0,1,1,0)].optimal,
			else:
				print 4,
		print

	return 
	
	

grilleA=gr.grille("exemple2.txt")
#grilleA.affichage((0,0))
pdm=PDM(grilleA)
iteration_value(pdm,0.99)
optimal_Pl(pdm,0.99)




