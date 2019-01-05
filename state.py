# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 15:45:48 2018

@author: Marc
"""
import grille as gr


class state:
	sword=0
	tresor=0
	key=0
	type=1
	#type=0 decision node , type=1 natural node
	position=list()
	stateType=""
	
	# Used for optimization methods
	vpast=0
	vnext=0
	#optimal policy , 0=top 1=domw 2=left 3=right
	optimal=-1
	variablePL=None



	def __init__(self,sword=0,tresor=0,key=0,position=None,type=2,grille=None,param=None):
		self.sword=sword
		self.tresor=tresor
		self.key=key
		self.position=position
		self.type=type
			
		if param=="fail"or param=="sucess":
			self.stateType=param
		else:
			self.stateType=grille.tab[position[0]][position[1]]


		return
		
		
	def update(self):
		self.vpast=self.vnext
		return
		
	def compare(self):
		return (self.vpast==self.vnext)

	def reset(self):
		self.vpast=0
		self.vnext=0
		self.optimal=-1
		self.variablePL=None
		return
		

