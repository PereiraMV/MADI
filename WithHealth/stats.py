from methods import *

def get_win_rate(pdm,sample=100):
	resultes={True:0,False:0}
	for i in range(sample):
		print "Solving grid n "+str(i)
		resultes[affichage_policy(pdm,affichage=False)]+=1
	print resultes
	return resultes

def get_all_size(pw=.3,po=.2,pc=.1,max_key=1,max_sword=1,max_portal=3):
	res=[]
#problemes avec PL

	for i in range(4,15):
		grilleA=gr.grille("grille.txt")
		grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
		pdm=PDM(grilleA)
		print "taille : "+str(grilleA.size[0])
		optimal_Pl(pdm,0.99,model_name="PDM"+str(i))
#		iteration_value(pdm,0.99)
		res.append(get_win_rate(pdm))
	return res
	
if __name__ == "__main__":
#	i=5
#	grilleA=gr.grille("grille.txt")
#	grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
#	pdm=PDM(grilleA)
#	print "taille : "+str(grilleA.size[0])
#	optimal_Pl(pdm,0.99,model_name="PDM"+str(i))
#
##	iteration_value(pdm,0.99)
#	get_win_rate(pdm)
#	
#	grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
#	pdm=PDM(grilleA)
#	optimal_Pl(pdm,0.99,model_name="PDM"+str(i+1))

	#generate grille
	res=get_all_size()
	print res
#	grilleA=gr.grille("grille.txt")
#	grilleA.generate_solvable(10,10,.3,.2,.1,1,1,3,nb_try=500)
	#grilleA.affichage((grilleA.size[0]-1,grilleA.size[0]-1))

	#Solve
#	pdm=PDM(grilleA)
	
#	iteration_value(pdm,0.99)
#	optimal_Pl(pdm,0.99)
#	Qlearning(pdm,0.99,lambda x:1.0/x,3000,eps=0.05)
	
	#affichage
#	affichage_policy(pdm)
#	affichage_one_state_policy(pdm,key=0,health=4,tresor=0,sword=0)
	
	#stats
#	get_win_rate(pdm)
	
	# 930 rows, 676 columns and 2244 nonzeros
