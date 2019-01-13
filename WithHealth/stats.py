from methods import *

def get_win_rate(pdm,sample=100):
	resultes={True:0,False:0}
	for i in range(sample):
		print "Solving grid n "+str(i)
		resultes[affichage_policy(pdm,affichage=False)]+=1
	print resultes
	return resultes

def get_all_size_iteration(pw=.3,po=.2,pc=.1,max_key=1,max_sword=1,max_portal=3):
	res=[[] for _ in range(4,13)]
	timed=[[] for _ in range(4,13)]
#problemes avec PL
	for i in range(4,13):
		for j in range(20):
			print j
			grilleA=gr.grille("grille.txt")
			grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
			pdm=PDM(grilleA)
			print "taille : "+str(grilleA.size[0])
			timed[i-4].append(timed_iteration_value(pdm,0.95))
			res[i-4].append(get_win_rate(pdm))
	return res,timed
	
#res4,timed4=get_all_size_iteration()
#test_res4=[[i[True] for i in j]for j in res4]
#test_time4=[[float(i) for i in j]for j in timed4]
#plt.boxplot(test_res4,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_res4))],[i for i in range(4,13)])
#plt.title("Nombre de succes value iteration en fonction de la taille de la grille")
#plt.savefig("iter_size_win.png")
#plt.show()
#
#plt.boxplot(test_time4,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_time4))],[i for i in range(4,13)])
#plt.title("Temps de resolution value iteration en fonction de la taille de la grille")
#plt.savefig("iter_size_time.png")
#plt.show()
	
def get_all_size_Q(pw=.3,po=.2,pc=.1,max_key=1,max_sword=1,max_portal=3):
	res=[[] for _ in range(4,13)]
	timed=[[] for _ in range(4,13)]

	for i in range(4,13):
		for j in range(20):
			print j
			grilleA=gr.grille("grille.txt")
			grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
			pdm=PDM(grilleA)
			print "taille : "+str(grilleA.size[0])
#			optimal_Pl(pdm,0.99,model_name="PDM"+str(i))
#			iteration_value(pdm,0.99)
			timed[i-4].append(timed_q_learning(pdm,0.95))
			res[i-4].append(get_win_rate(pdm))
	return res,timed
	
#res5,timed5=get_all_size_Q()
#test_res5=[[i[True] for i in j]for j in res5]
#test_time5=[[float(i) for i in j]for j in timed5]
#plt.boxplot(test_res5,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_res5))],[i for i in range(4,13)])
#plt.title("Nombre de succes q-learning en fonction de la taille de la grille")
#plt.savefig("q_size_win.png")
#plt.show()
#
#plt.boxplot(test_time5,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_time5))],[i for i in range(4,13)])
#plt.title("Temps de resolution q-learning en fonction de la taille de la grille")
#plt.savefig("q_size_time.png")
#plt.show()
	
def get_all_gam_iter(gam=0.99,i=8):
	timed=[[] for _ in range(49,100,5)]
	res=[[] for _ in range(49,100,5)]
	cpt=0
	for gam in range(49,100,5):
		for j in range(20):#20
			grilleA=gr.grille("grille.txt")
			grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
			pdm=PDM(grilleA)
			print "taille : "+str(grilleA.size[0])
			print 'gam ' + str(gam)
			print 'j'+str(j)
			timed[cpt].append(timed_iteration_value(pdm,gam/100.0))
			res[cpt].append(get_win_rate(pdm))
		cpt+=1
	return res,timed

#res,timed=get_all_gam_iter(i=7)
#test_res=[[i[True] for i in j]for j in res]
#test_time=[[float(i) for i in j]for j in timed]
#plt.boxplot(test_res,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_res))],[i/100.0 for i in range(49,100,5)])
#plt.title("Nombre de succes value iteration en fonction de gamma")
#plt.savefig("iter_gamma_win.png")
#plt.show()
#
#plt.boxplot(test_time,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_time))],[i/100.0 for i in range(49,100,5)])
#plt.title("Temps de resolution value iteration en fonction de gamma")
#plt.savefig("iter_gamma_time.png")
#plt.show()

def get_all_gam_q(gam=0.99,i=8):
	timed=[[] for _ in range(49,100,5)]
	res=[[] for _ in range(49,100,5)]
	cpt=0
	for gam in range(49,100,5):
		for j in range(20):#20
			grilleA=gr.grille("grille.txt")
			grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
			pdm=PDM(grilleA)
			print "taille : "+str(grilleA.size[0])
			print 'gam ' + str(gam)
			timed[cpt].append(timed_q_learning(pdm,gam/100.0))
			res[cpt].append(get_win_rate(pdm))
		cpt+=1
	return res,timed
	
#res2,timed2=get_all_gam_q(i=7)
#test_res2=[[i[True] for i in j]for j in res2]
#test_time2=[[float(i) for i in j]for j in timed2]
#plt.boxplot(test_res2,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_res2))],[i/100.0 for i in range(49,100,5)])
#plt.title("Nombre de succes q-learning en fonction de gamma")
#plt.savefig("q_gamma_win.png")
#plt.show()
#
#plt.boxplot(test_time2,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_time2))],[i/100.0 for i in range(49,100,5)])
#plt.title("Temps de resolution q-learning en fonction de gamma")
#plt.savefig("q_gamma_time.png")
#plt.show()

def get_all_timer_q(timer=10000,i=8):
	timed=[[] for _ in range(3000,11001,2000)]
	res=[[] for _ in range(3000,11001,2000)]
	cpt=0
	for timer in range(3000,11001,2000):
		for j in range(2):#20
			grilleA=gr.grille("grille.txt")
			grilleA.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=5000)
			pdm=PDM(grilleA)
			print "taille : "+str(grilleA.size[0])
			print 'iteration ' + str(timer)
			timed[cpt].append(timed_q_learning(pdm,gam=0.95,timer=timer))
			res[cpt].append(get_win_rate(pdm))
		cpt+=1
	return res,timed
	
#res3,timed3=get_all_timer_q(i=7)
#test_res3=[[i[True] for i in j]for j in res3]
#test_time3=[[float(i) for i in j]for j in timed3]
#plt.boxplot(test_res3,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_res3))],[i for i in range(3000,11001,2000)])
#plt.title("Nombre de succes q-learning en fonction du nombre d'iterations")
#plt.savefig("q_iter_win.png")
#plt.show()
#
#plt.boxplot(test_time3,showmeans=True)
#plt.xticks([ i+1 for i in range(len(test_time3))],[i for i in range(3000,11001,2000)])
#plt.title("Temps de resolution q-learning en fonction du nombre d'iterations")
#plt.savefig("q_iter_time.png")
#plt.show()
	
	
	
def timed_q_learning(pdm,gam=0.99,taux=lambda x:1.0/x,timer=10000,eps=0.05):
	t0=time.time()
	Qlearning(pdm,0.99,lambda x:1.0/x,10000,eps=0.05)
	t='%.2f' % (time.time()-t0)
	return t

def timed_iteration_value(pdm,gam,eps=0.000001):
	t0=time.time()
	iteration_value(pdm,gam)
	t='%.2f' % (time.time()-t0)
	return t
	
	


#if __name__ == "__main__":
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
#	res=get_all_size()
#	print res
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
