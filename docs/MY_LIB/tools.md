```  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_coor_box(lines):
	X=(float(lines.split()[5]))
	Y=(float(lines.split()[6]))
	Z=(float(lines.split()[7]))
	return X,Y,Z
def get_coor_pdb(lines):
	X=(float(lines.split()[6]))
	Y=(float(lines.split()[7]))
	Z=(float(lines.split()[8]))
	return X,Y,Z

class select_res_by_dis:
	def __init__(self,targetfile,lig,select_dis,z,ligtype='',filetype='pdb',atomname=''):
		self.targetfile=targetfile
		self.lig=lig
		self.select_dis=select_dis
		self.z=z
		self.ligtype=ligtype
		self.filetype=filetype
		self.atomname=atomname
	def dis2lig(self):
		import math
		res=[]
		pdbline=[]
		atom=[]
		select_index=[]
		with open(self.targetfile) as pdb:
			line = pdb.readlines()
			for lines in line:
				if str(self.ligtype) in lines.split()[0] and (lines.split()[3] in self.lig):
					X,Y,Z = get_coor_box(lines) if self.filetype=='box' else get_coor_pdb(lines)
					for lines in line:
						if 'ATOM' in lines.split()[0]:
							x,y,z= get_coor_box(lines) if self.filetype=='box' else get_coor_pdb(lines)
							dis=math.sqrt(math.pow(abs(x-X), 2)+math.pow(abs(y-Y), 2)+math.pow(abs(z-Z), 2))
							if dis <= self.select_dis:
								if self.ligtype =='HETATM':
									res.append(''.join(lines.split()[3])+':'+''.join(lines.split()[5]))
									select_index.append(''.join(lines.split()[5]))
								else:
									res.append(''.join(lines.split()[3])+':'+''.join(lines.split()[4]))
									select_index.append(''.join(lines.split()[4]))
			select=set(res)
			set(select_index)
			for lines in line:
				try:
					index=(''.join(lines.split()[4]))
					if index in select_index:
						coor=''.join(lines)[0:62] 
						end=''.join(lines)[66:]
						lines=(f'{coor}1.00{end}')
						pdbline.append(lines)
						atom.append(str(int(''.join(lines.split()[1]))-self.z)+' ')
				except:
					continue
		return select,pdbline,atom
	def dis2atom(self):
		import math
		res=[]
		pdbline=[]
		atom=[]
		select_index=[]
		with open(self.targetfile) as pdb:
			line = pdb.readlines()
			for lines in line:
				if str(self.ligtype) in lines.split()[0] and (lines.split()[3] in self.lig) and (lines.split()[2] in self.atomname):
					X,Y,Z = get_coor_box(lines) if self.filetype=='box' else get_coor_pdb(lines)
					for lines in line:
						if 'ATOM' in lines.split()[0]:
							x,y,z= get_coor_box(lines) if self.filetype=='box' else get_coor_pdb(lines)
							dis=math.sqrt(math.pow(abs(x-X), 2)+math.pow(abs(y-Y), 2)+math.pow(abs(z-Z), 2))
							if dis <= self.select_dis:
								if self.ligtype =='HETATM':
									res.append(''.join(lines.split()[3])+':'+''.join(lines.split()[5]))
									select_index.append(''.join(lines.split()[5]))
								else:
									res.append(''.join(lines.split()[3])+':'+''.join(lines.split()[4]))
									select_index.append(''.join(lines.split()[4]))
			select=set(res)
			set(select_index)
			for lines in line:
				try:
					index=(''.join(lines.split()[4]))
					if index in select_index:
						coor=''.join(lines)[0:62] 
						end=''.join(lines)[66:]
						lines=(f'{coor}1.00{end}')
						pdbline.append(lines)
						atom.append(str(int(''.join(lines.split()[1]))-self.z)+' ')
				except:
					continue
		return select,pdbline,atom
	
def takeSecond(elem):
	return elem[1]
def TotleSelect(score):
	scorefaile=[]
	with open(score,'r') as scoreread:
		line = scoreread.readlines()[2:]
		for lines in line:
			scorefaile.append(lines.split())
		scorefaile.sort(key=takeSecond)
		low=str((' '.join(scorefaile[-1])).split()[-1])
		print(low)
	scorefaile=''
```  
