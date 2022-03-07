```  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math,os
from Bio.PDB import *


class select_res_by_dis:
	def __init__(self,targetfile,lig,select_dis,z,atomname='',except_res=[],save=False):
		self.targetfile=targetfile
		self.lig=lig
		self.select_dis=select_dis
		self.z=z
		self.atomname=atomname
		self.except_res=except_res
		self.save=save
	def takeSecond_(elem):
		return elem.split(',')[1]
	def dis2lig(self):
		n=0
		res_list=[]
		atom_list=[]
		select_list=[]
		ligatom=[]
		res_except=self.except_res
		res_except.append(self.lig)
		parser = PDBParser(PERMISSIVE=True)
		structure_name = (str(self.targetfile).strip('pdb'))[0:4]
		fileName = self.targetfile
		pdb = parser.get_structure(structure_name,fileName)
		atomList = Selection.unfold_entities(pdb, 'A')
		for residue in pdb.get_residues():
			if n == 0:
				if residue.get_resname() == self.lig:
					n+=1
					ligatom_list=Selection.unfold_entities(residue, "A")
					for i in ligatom_list:
						ligatom.append(i.get_name())
					for atom in residue:
						if atom.get_name() in ligatom:
							coor=atom.get_coord()
							ns=NeighborSearch(atomList).search(coor,self.select_dis,level='R')
							select_list+=ns
							for i in ns:
								res_name=i.get_resname()
								res_id=i.get_id()[1]
								if res_name not in res_except:
									res_list.append(f'{res_name},{res_id}')
		re_list=list(set(res_list))
		io = PDBIO()
		io.set_structure(pdb)
		class Select_pdb(Select):
		    def accept_residue(self, residue):
		        if residue in select_list:
		            return 1
		        else:
		            return 0
		if self.save==True:
			io.save(f"select_{structure_name}.pdb",Select_pdb())
		for resdue in select_list:
			atoms = resdue.get_atoms()
			for i in atoms:
				atom_list.append(i.get_serial_number()-self.z)
		at_list=list(set(atom_list))
		at_list.sort()
		re_list.sort(key=select_res_by_dis.takeSecond_)
					
		return re_list,at_list
	def dis2atom(self):
		n=0
		res_list=[]
		atom_list=[]
		select_list=[]
		res_except=self.except_res
		res_except.append(self.lig)
		parser = PDBParser(PERMISSIVE=True)
		structure_name = (str(self.targetfile).strip('pdb'))[0:4]
		fileName = self.targetfile
		pdb = parser.get_structure(structure_name,fileName)
		atomList = Selection.unfold_entities(pdb, 'A')
		for residue in pdb.get_residues():
			if n == 0:
				if residue.get_resname() == self.lig:
					n+=1
					for atom in residue:
						if atom.get_name() in self.atomname:
							coor=atom.get_coord()
							ns=NeighborSearch(atomList).search(coor,self.select_dis,level='R')
							select_list+=ns
							for i in ns:
								res_name=i.get_resname()
								res_id=i.get_id()[1]
								if res_name not in res_except:
									res_list.append(f'{res_name},{res_id}')
		re_list=list(set(res_list))
		io = PDBIO()
		io.set_structure(pdb)
		class Select_pdb(Select):
		    def accept_residue(self, residue):
		        if residue in select_list:
		            return 1
		        else:
		            return 0
		if self.save==True:
			io.save(f"select_{structure_name}.pdb",Select_pdb())
		for resdue in select_list:
			atoms = resdue.get_atoms()
			for i in atoms:
				atom_list.append(i.get_serial_number()-self.z)
		at_list=list(set(atom_list))
		at_list.sort()
		re_list.sort(key=select_res_by_dis.takeSecond_)
		
		return re_list,at_list
	
# def takeFirst(elem):
# 	return elem[0]
# def takeSecond(elem):
# 	return elem[1]
# def TotleSelect(score):
# 	scorefaile=[]
# 	with open(score,'r') as scoreread:
# 		line = scoreread.readlines()[2:]
# 		for lines in line:
# 			scorefaile.append(lines.split())
# 		scorefaile.sort(key=takeSecond)
# 		low=str((' '.join(scorefaile[-1])).split()[-1])
# 		print(low)
# 	scorefaile=''
```  
