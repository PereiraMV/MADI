from methods import *
import sys

if __name__ == "__main__":
	args=sys.argv
	del args[0]
	if len(args)==0:
		print "Utilisation : python main.py filename"
	a=gr.grille(args[0])
	ans=str(raw_input("Generer une grille aléatoire ? o/n"))
	if ans=="o":
		i=str(raw_input("Quelle taille de grille ? (unique nombre)"))
		a.generate_solvable(i,i,.3,.2,.1,1,1,3,nb_try=500)
	pdm=PDM(a)
	print "Que faire avec cette grille ?"
	ans=str(raw_input("1: Jouer\n2:Résoudre Iteration Value\n3:Résoudre PL\n4:Résoudre Q-learning"))
	if ans==1:
		pdm.play()
	if ans==2:
		iteration_value(pdm,0.99)
	if ans==3:
		optimal_Pl(pdm,0.99)
	if ans==4:
		Qlearning(pdm,0.99,lambda x:1.0/x,10000,eps=0.05)