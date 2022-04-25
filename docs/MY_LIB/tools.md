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
		#res_except.append(self.lig)
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
		        if f'{residue.get_resname()},{residue.get_id()[1]}' in re_list:
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
	def dis2coor(self):
		resdict = {'GLY': 'CA', 
			   'SER': 'CB',
               'ALA': 'CB',
			   'ARG': 'CZ',
			   'HID': 'CG',
			   'TRP': 'CD2',
			   'PHE': 'CG',
			   'CYS': 'CB',
			   'MET': 'CE',
			   'LEU': 'CG',
			   'VAL': 'CB',
			   'ASN': 'CG',
			   'GLU': 'CD',
			   'LYS': 'CE',
			   'GLN': 'CD',
			   'ILE': 'CG1',
			   'THR': 'CB',
			   'PRO': 'CG',
			   'TYP': 'CZ',
			   'ASP': 'CG'}
		RES=['GLY','SER','ALA','ARG','HID','TRP','PHE','CYS','MET','LEU','VAL','ASN','GLU','LYS','GLN','ILE','THR','PRO','TYP','ASP']
		n=0
		res_coor=[]
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
					for atom_lig in residue:
						atomname=atom_lig.get_name()
						if atomname in self.atomname:
							coor=atom_lig.get_coord()
							ns=NeighborSearch(atomList).search(coor,self.select_dis,level='R')
							for i in ns:
								resname=i.get_resname()
								if resname in RES:
									MATOM=resdict[resname]
									for atom in i:
										if atom.get_name() == MATOM: 
											M_coor=atom.get_coord()
											COOR=','.join(str(i) for i in M_coor-coor)
											dis=atom-atom_lig
											res_coor.append(f'{atomname},{resname},{dis}')
		rescoor=list(set(res_coor))
		rescoor.sort()
		return rescoor
def down_pdb_fasta(pdbid):#下载晶体对应fasta
	subprocess.run(f'nohup wget https://www.rcsb.org/fasta/entry/{pdbid} &',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
def seq_ded(fasta,key): #序列去重，输入fasta文件
	from Bio import SeqIO
	import argparse
	old = SeqIO.parse(f"{fasta}", "fasta")
	new = open("ded.fasta", "w")
	new_list=[]
	open("ded.fasta", "w").write('')
	if key == 'id':
		for i in old:
			if i.id.split('_')[0] not in new_list:
				new.write(">"+(i.id).split('_')[0]+"\n")
				new.write(str(i.seq)+"\n")
				new_list.append(i.id.split('_')[0])
	if key == 'seq':
		for i in old:
			if str(i.seq) not in new:
				new.write(">"+i.id+"\n")
				new.write(str(i.seq)+"\n")
				new_list.append(i.id.split('_')[0])
	new.close()
def seq_len(fasta,num): #序列去短，输入fasta文件
	from Bio import SeqIO
	import argparse
	old = SeqIO.parse(f"{fasta}", "fasta")
	new = open("len.fasta", "w")
	open("len.fasta", "w").write('')
	for i in old:
		if len(i.seq)>num:
			new.write(">"+i.id+"\n")
			new.write(str(i.seq)+"\n")
	new.close()
def pdb_only_chain(pdb,path):#提取晶体中第一条链的结构
	import os
	if os.path.exists(path)==0:
		os.makedirs(path)
	n=0
	parser = PDBParser(PERMISSIVE=True)
	io=PDBIO()
	chain_name=''
	structure_name = (str(pdb).strip('pdb'))[0:4]
	fileName = pdb
	structure = parser.get_structure(structure_name,fileName)
	for chain in structure.get_chains():	
		if n < 1:
			chain_name=chain
			n+=1
	io.set_structure(structure)
	class Select_chain(Select):
	    def accept_chain(self, chain):
	        if chain == chain_name:
	            return 1
	        else:
	            return 0
	io.save(f'{path}/{structure_name}.pdb',Select_chain())
def get_dir_files():
	for root, dirs, files in os.walk('.'): 
		print(files)
		return files
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
