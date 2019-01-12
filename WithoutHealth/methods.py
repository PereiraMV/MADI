from PDM import *

import numpy as np
import time 
from gurobipy import *


def timer(f):
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
				print pdm.listState[((i,j),0,0,0,0)].optimal,
			else:
				print 4,
		print

	return 
	
	

	
def next_state(Trans,indice,stateA):
	
	transPlayer=Trans[(stateA.position,stateA.sword,stateA.key,stateA.tresor,stateA.type)][indice]
	
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
	Trans=pdm.listTrans
	for key,lisTrans in Trans.items():
		if key[4]==0:
			Trans[key]=[trans for trans in lisTrans if trans!=None]
			

	for key,state in pdm.listState.items():
		state.reset()
		state.initiateQl(len(Trans[key]))

	initialState=pdm.listState[((pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,0,0)]
	for i in range (0,timer):
		#print("###############################################"+str(i))
		stateA=pdm.listState[((pdm.grille.size[0]-1,pdm.grille.size[1]-1),0,0,0,0)]
		it=1
		epsilon=0.1
		maxdiff=0
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

			
			
			#update of epsilon
			if (epsilon<=eps):
				epsilon=eps
			else:
				epsilon=epsilon-0.0001
				

			stateA=stateB
			it+=1

				
			
		
		
		####put solution in optimal
	for i in range(pdm.grille.size[0]):
		for j in range(pdm.grille.size[1]):
			if pdm.grille.tab[i][j]!='M' and pdm.grille.tab[i][j]!='P' and pdm.grille.tab[i][j]!='W' and  pdm.grille.tab[i][j]!='C':
				#position sword key tresor type
				statecurr=pdm.listState[((i,j),0,0,0,0)]
				positionCurr=statecurr.position
				maxi=np.argmax(statecurr.Ql)
				stateNeig=Trans[((i,j),0,0,0,0)][maxi].listState[0]
				positionNeig=stateNeig.position

				if positionNeig[0]==positionCurr[0]-1 and positionNeig[1]==positionCurr[1]:
					statecurr.optimal=0
					print "0",
				if positionNeig[0]==positionCurr[0]+1 and positionNeig[1]==positionCurr[1]:
					statecurr.optimal=1
					print "1",
				if positionNeig[0]==positionCurr[0] and positionNeig[1]==positionCurr[1]-1:
					statecurr.optimal=2
					print "2",
				if positionNeig[0]==positionCurr[0] and positionNeig[1]==positionCurr[1]+1:
					statecurr.optimal=3
					print "3",
			else:
				print "4",
		print
	
		
	pdm.grille.affichage((0,0))
		
	return
	

grilleA=gr.grille("exemple2.txt")
#grilleA.affichage((0,0))
pdm=PDM(grilleA)
#iteration_value(pdm,0.99)
optimal_Pl(pdm,0.8)
Qlearning(pdm,0.8,taux=lambda x:1.0/x,timer=30000,eps=0.05)
state=pdm.listState[((3,2),0,1,0,1)]
print(state.Ql)


