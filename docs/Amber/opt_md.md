```
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 16:10:22 2021

@author: baijie
"""
import sys,getopt,os,datetime,subprocess
from re       import search as re_search
def usage():										      ### help documents
	useinfo = '''
	-h:\thelp documents.\n
	-i:\tinput pdb file name like <1AB2.PDB>.\n
	-j:\tthreads like <3>.\n
	-m:\tchose sander or pmemd \n
	-u:\tuse cuda like <cuda>
	-n:\t
	-amd
	'''
	print (useinfo)
	exit()
opts,args = getopt.getopt(sys.argv[1:],'hi:m:j:u:n:amd:')
targetfile = ''
duration = ''
ligands =''
number = ''
restrain =''
length = ''
steptime = ''
proce = 'pmemd'
index = 0
lign = 0
threads = ''
GPU = '.cuda'		
mpi = ''
n = ''		
amd=0				 
for op,value in opts:
	if op == '-i':
		targetfile = str(value)
		print ('The target pdb file is: '+targetfile)
	elif op == '-m':
		proce = value 
	elif op == '-j':
		threads = str('mpirun -np '+value+' ')
		mpi = '.MPI'
	elif op == '-u':
		GPU = '.'+value
	elif op == '-n':
		n = value
	elif op == '-amd':
		amd=1
	elif op == '-h':
		usage()
name = str(targetfile).split('.pdb')[0]
print(name)
with open(f'in/{name}_box.pdb','r') as seqread:
	line = seqread.readlines()
	for lines in line:
		li = lines.split()
		try:
			if ('OXT') in li:
				seqR=(lines.split('OXT')[1].split()[1])
			if ('ATOM') in li:
				atoms=li[1]
		except:
			continue
order=str(seqR)
open('in/min1.in','w').write(f" &cntrl  \n"\
							 f"  imin=1, \n"\
							 f"  maxcyc=10000, \n"\
							 f"  ncyc=10000, \n"\
							 f"  ntb=1, \n"\
							 f"  ntr=1,\n"\
							 f"  restraintmask=':1-{order}@CA,N,C', \n"\
							 f"  restraint_wt=50.0,\n"\
							 f"  cut=12.0 \n"\
							 f" / \n END")
open('in/min2.in','w').write(f" &cntrl  \n"\
							 f"  imin=1, \n"\
							 f"  maxcyc=10000, \n"\
							 f"  ncyc=10000, \n"\
							 f"  ntb=1, \n"\
							 f"  cut=12.0 \n"\
							 f" / \n END")
open('in/heat.in','w').write(f'explicit solvent initial heating: 50ps\n'\
							 f' &cntrl\n'\
							 f'  imin=0,\n'\
							 f'  irest=0,\n'\
							 f'  nstlim=2500,\n'\
							 f'  dt=0.002,\n'\
							 f'  ntc=2,\n'\
							 f'  ntf=2,\n'\
							 f'  ntx=1,\n'\
							 f'  cut=12.0,\n'\
							 f'  ntb=1,\n'\
							 f'  ntpr=500,\n'\
							 f'  ntwx=500,\n'\
							 f'  ntt=3,\n'\
							 f'  gamma_ln=2.0,\n'\
							 f'  tempi=0.0,\n'\
							 f'  temp0=300.0,\n'\
							 f'  ig=-1,\n'\
							 f'  ntr=1,\n'\
							 f"  restraintmask=':1-{order}@CA,N,C',\n"\
							 f'  restraint_wt=50.0,\n'\
							 f'  iwrap=1\n'\
							 f'  nmropt=1\n'\
							 f'  /\n'\
							 f"  &wt TYPE='TEMP0',\n"\
							 f'  ISTEP1=0,\n'\
							 f'  ISTEP2=2500,\n'\
							 f'  VALUE1=0.0,\n'\
							 f'  VALUE2=300.0,\n'\
							 f'  /\n'\
							 f"  &wt TYPE = 'END'\n"\
							 f'  / \n'\
							 f'  END')
open('in/press.in','w').write(f'explicit solvent density: 50ps\n'\
								f' &cntrl\n'\
								f'  imin=0,\n'\
								f'  irest=1,\n'\
								f'  ntx=5,\n'\
								f'  nstlim=25000,\n'\
								f'  dt=0.0002,\n'\
								f'  ntc=2,\n'\
								f'  ntf=2,\n'\
								f'  cut=8.0,\n'\
								f'  ntb=2,\n'\
								f'  ntp=1,\n'\
								f'  taup=2.0,\n'\
								f'  ntpr=500,\n'\
								f'  ntwx=500,\n'\
								f'  ntt=3,\n'\
								f'  gamma_ln=2.0,\n'\
								f'  temp0=300.0,\n'\
								f'  ig=-1,\n'\
								f'  ntr=1,\n'\
								f"  restraintmask=':1-{order}@CA,N,C',\n"\
								f'  restraint_wt=50.0,\n'\
								f'  iwrap=1\n  / \n END')
open('in/eq.in','w').write(f'&cntrl\n'\
							 f'  imin=0,\n'\
							 f'  irest=1,\n'\
							 f'  ntx=5,\n'\
							 f'  nstlim=2500000,'\
							 f'  dt=0.002,\n'\
							 f'  ntc=2,\n'\
							 f'  ntf=2,\n'\
							 f'  cut=10.0,\n'\
							 f'  ntb=2,\n'\
							 f'  ntp=1,\n'\
							 f'  taup=2.0,\n'\
							 f'  ntpr=500,\n'\
							 f'  ntwx=500,\n'\
							 f'  ntwr=50,\n'\
							 f'  ntt=3,\n'\
							 f'  gamma_ln=2.0,\n'\
							 f'  ntr=1,\n'\
							 f'  temp0=300.0,\n'\
							 f"  restraintmask=':1-{order}@CA,N,C',\n"\
							 f'  restraint_wt=500.0,\n'\
							 f'  iwrap=1\n'\
							 f'  / \n'\
							 f' END')
open('in/md_1.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=50.0,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_2.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=25.0,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_3.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=10.0,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_4.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=5.0,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_5.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=2.0,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_6.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=1.0,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_7.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.5,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_8.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.2,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_9.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.1,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_10.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.05,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_11.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.02,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_12.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.01,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_13.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.005,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_14.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.002,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md_15.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=1000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=10.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  ntr=1,\n'\
 						   f"  restraintmask=':1-{order}@CA,N,C',\n"\
 						   f'  restraint_wt=0.001,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
open('in/md.in','w').write(f'explicit solvent production run\n'\
 						   f'&cntrl\n'\
 						   f'  imin=0,\n'\
 						   f'  irest=1,\n'\
 						   f'  ntx=5,\n'\
 						   f'  nstlim=50000000,\n'\
 						   f'  dt=0.002,\n'\
 						   f'  ntc=2,\n'\
 						   f'  ntf=2,\n'\
 						   f'  cut=12.0,\n'\
 						   f'  ntb=2,\n'\
 						   f'  ntp=1,\n'\
 						   f'  taup=2.0,\n'\
 						   f'  ntpr=5000,\n'\
 						   f'  ntwx=5000,\n'\
 						   f'  ntwr=50000,\n'\
 						   f'  ntt=3,\n'\
 						   f'  gamma_ln=2.0,\n'\
 						   f'  temp0=300.0,\n'\
 						   f'  ig=-1,\n'\
 						   f'  iwrap=1\n'\
 						   f'  / \n END')
if os.path.exists('out')==0:
 	os.makedirs('out')
os.environ['CUDA_VISIBLE_DEVICES']=str(n)
def sub(cmd):
	run=subprocess.run(cmd,stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=None, universal_newlines=False,shell=True)
	return run
if os.path.exists(f'out/{name}_box_min1.rst')==0:
	print('run min1 ... waiting\n.....')
	starttime = datetime.datetime.now()
	min1=f'pmemd.cuda -O -i in/min1.in -o out/{name}_box_min1.mdout -p in/{name}_box.prmtop -c in/{name}_box.inpcrd -r out/{name}_box_min1.rst -ref in/{name}_box.inpcrd'
	check=sub(min1)
	if check.returncode != 0:
		print('This error does not usually occur, please check your input file and command')
		exit
	amb=f'ambpdb -p in/{name}_box.prmtop -c out/{name}_box_min1.rst > out/{name}_box_min1.pdb'
	sub(amb)
	endtime = datetime.datetime.now()
	print('mining1 complete')
	print (endtime - starttime)
	# ###############	min1
if os.path.exists(f'out/{name}_box_min2.rst')==0:
	print('run min2 ... waiting\n.....')
	starttime = datetime.datetime.now()
	min2=f'pmemd.cuda -O -i in/min2.in -o out/{name}_box_min2.mdout -p in/{name}_box.prmtop -c out/{name}_box_min1.rst -r out/{name}_box_min2.rst -ref out/{name}_box_min1.rst'
	check=sub(min2)
	if check.returncode != 0:
		print('This error does not usually occur, please check your input file and command')
		exit
	amb=f'ambpdb -p in/{name}_box.prmtop -c out/{name}_box_min2.rst > out/{name}_box_min2.pdb'
	sub(amb)
	endtime = datetime.datetime.now()
	print('mining2 complete')
	print (endtime - starttime)
	# ###############	min2
if os.path.exists(f'out/{name}_box_heat.rst')==0:
	print('run heat ... waiting\n.....')
	starttime = datetime.datetime.now()
	heat=f'pmemd.cuda -O -i in/heat.in -o out/{name}_box_heat.mdout -p in/{name}_box.prmtop -c out/{name}_box_min2.rst -r out/{name}_box_heat.rst -x out/{name}_box_heat.nc -ref out/{name}_box_min2.rst'
	check=sub(heat)
	if check.returncode != 0:
		print('Try to lower step')
		open('in/heat.in','w').write(f'explicit solvent initial heating: 50ps\n'\
								 f' &cntrl\n'\
								 f'  imin=0,\n'\
								 f'  irest=0,\n'\
								 f'  nstlim=25000,\n'\
								 f'  dt=0.0002,\n'\
								 f'  ntc=2,\n'\
								 f'  ntf=2,\n'\
								 f'  ntx=1,\n'\
								 f'  cut=12.0,\n'\
								 f'  ntb=1,\n'\
								 f'  ntpr=500,\n'\
								 f'  ntwx=500,\n'\
								 f'  ntt=3,\n'\
								 f'  gamma_ln=2.0,\n'\
								 f'  tempi=0.0,\n'\
								 f'  temp0=300.0,\n'\
								 f'  ig=-1,\n'\
								 f'  ntr=1,\n'\
								 f"  restraintmask=':1-{order}@CA,N,C',\n"\
								 f'  restraint_wt=50.0,\n'\
								 f'  iwrap=1\n'\
								 f'  nmropt=1\n'\
								 f'  /\n'\
								 f"  &wt TYPE='TEMP0',\n"\
								 f'  ISTEP1=0,\n'\
								 f'  ISTEP2=25000,\n'\
								 f'  VALUE1=0.0,\n'\
								 f'  VALUE2=300.0,\n'\
								 f'  /\n'\
								 f"  &wt TYPE = 'END'\n"\
								 f'  / \n'\
								 f'  END')
		check=sub(heat)
		if check.returncode != 0:
			print('Try to lower step')
			open('in/heat.in','w').write(f'explicit solvent initial heating: 50ps\n'\
									 f' &cntrl\n'\
									 f'  imin=0,\n'\
									 f'  irest=0,\n'\
									 f'  nstlim=250000,\n'\
									 f'  dt=0.00002,\n'\
									 f'  ntc=2,\n'\
									 f'  ntf=2,\n'\
									 f'  ntx=1,\n'\
									 f'  cut=12.0,\n'\
									 f'  ntb=1,\n'\
									 f'  ntpr=500,\n'\
									 f'  ntwx=500,\n'\
									 f'  ntt=3,\n'\
									 f'  gamma_ln=2.0,\n'\
									 f'  tempi=0.0,\n'\
									 f'  temp0=300.0,\n'\
									 f'  ig=-1,\n'\
									 f'  ntr=1,\n'\
									 f"  restraintmask=':1-{order}@CA,N,C',\n"\
									 f'  restraint_wt=50.0,\n'\
									 f'  iwrap=1\n'\
									 f'  nmropt=1\n'\
									 f'  /\n'\
									 f"  &wt TYPE='TEMP0',\n"\
									 f'  ISTEP1=0,\n'\
									 f'  ISTEP2=250000,\n'\
									 f'  VALUE1=0.0,\n'\
									 f'  VALUE2=300.0,\n'\
									 f'  /\n'\
									 f"  &wt TYPE = 'END'\n"\
									 f'  / \n'\
									 f'  END')
			check=sub(heat)
			if check.returncode != 0:
				print('Try to lower step')
				open('in/heat.in','w').write(f'explicit solvent initial heating: 50ps\n'\
										 f' &cntrl\n'\
										 f'  imin=0,\n'\
										 f'  irest=0,\n'\
										 f'  nstlim=2500000,\n'\
										 f'  dt=0.000002,\n'\
										 f'  ntc=2,\n'\
										 f'  ntf=2,\n'\
										 f'  ntx=1,\n'\
										 f'  cut=12.0,\n'\
										 f'  ntb=1,\n'\
										 f'  ntpr=500,\n'\
										 f'  ntwx=500,\n'\
										 f'  ntt=3,\n'\
										 f'  gamma_ln=2.0,\n'\
										 f'  tempi=0.0,\n'\
										 f'  temp0=300.0,\n'\
										 f'  ig=-1,\n'\
										 f'  ntr=1,\n'\
										 f"  restraintmask=':1-{order}@CA,N,C',\n"\
										 f'  restraint_wt=50.0,\n'\
										 f'  iwrap=1\n'\
										 f'  nmropt=1\n'\
										 f'  /\n'\
										 f"  &wt TYPE='TEMP0',\n"\
										 f'  ISTEP1=0,\n'\
										 f'  ISTEP2=2500000,\n'\
										 f'  VALUE1=0.0,\n'\
										 f'  VALUE2=300.0,\n'\
										 f'  /\n'\
										 f"  &wt TYPE = 'END'\n"\
										 f'  / \n'\
										 f'  END')
				check=sub(heat)
				if check.returncode != 0:
					print('Can not fix err, please check your structure')
					exit
	endtime = datetime.datetime.now()
	print('heating complete')
	print (endtime - starttime)
	# ##############	heat
if os.path.exists(f'out/{name}_box_press.rst')==0:
	# print('run press ... waiting\n.....')
	starttime = datetime.datetime.now()
	press=f'pmemd.cuda -O -i in/press.in -o out/{name}_box_press.mdout -p in/{name}_box.prmtop -c out/{name}_box_heat.rst -r out/{name}_box_press.rst -x out/{name}_box_press.nc -ref out/{name}_box_heat.rst'
	check=sub(press)
	endtime = datetime.datetime.now()
	print('pressing complete')
	print (endtime - starttime)
	##############	press
if os.path.exists(f'out/{name}_box_eq.rst')==0:
	print('run eq ... waiting\n.....')
	starttime = datetime.datetime.now()
	eq=f'pmemd.cuda -O -i in/eq.in -o out/{name}_box_eq.mdout -p in/{name}_box.prmtop -c out/{name}_box_press.rst -ref out/{name}_box_press.rst -r out/{name}_box_eq.rst -x out/{name}_box_eq.nc'
	req=f'pmemd.cuda -O -i in/eq.in -o out/{name}_box_eq.mdout -p in/{name}_box.prmtop -c out/{name}_box_eq.rst -ref out/{name}_box_eq.rst -r out/{name}_box_eq.rst -x out/{name}_box_eq.nc'
	check=sub(eq)
	if check.returncode != 0:
		print('try to restart' )
		check=check=sub(req)
		if check.returncode != 0:
			print('try to restart' )
			check=check=sub(req)
			if check.returncode != 0:
				print('try to restart' )
				check=check=sub(req)
				if check.returncode != 0:
					print('try to restart' )
					check=check=sub(req)
					if check.returncode != 0:
						print('try to restart' )
						check=check=sub(req)
						if check.returncode != 0:
							print('try to restart' )
							check=check=sub(req)
							if check.returncode != 0:
								print('abnormal, please check')
								exit
	amb=f'ambpdb -p in/{name}_box.prmtop -c out/{name}_box_eq.rst > out/{name}_box_eq.pdb'
	sub(amb)
	endtime = datetime.datetime.now()
	print('eq complete')
	print (endtime - starttime)
	##############	eq
if os.path.exists(f'out/{name}_box_md_1.rst')==0:
	print('run md_1 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md1=f'pmemd.cuda -O -i in/md_1.in -o out/{name}_box_md_1.mdout -p in/{name}_box.prmtop -c out/{name}_box_eq.rst -ref out/{name}_box_eq.rst -r out/{name}_box_md_1.rst -x out/{name}_box_md_1.nc'
	check=sub(md1)
	endtime = datetime.datetime.now()
	print('md_1 complete')
	print (endtime - starttime)
	##############	md_1
if os.path.exists(f'out/{name}_box_md_2.rst')==0:
	print('run md_2 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md2=f'pmemd.cuda -O -i in/md_2.in -o out/{name}_box_md_2.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_1.rst -ref out/{name}_box_md_1.rst -r out/{name}_box_md_2.rst -x out/{name}_box_md_2.nc'
	check=sub(md2)
	endtime = datetime.datetime.now()
	print('md_2 complete')
	print (endtime - starttime)
	##############	md_2
if os.path.exists(f'out/{name}_box_md_3.rst')==0:
	print('run md_3 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md3=f'pmemd.cuda -O -i in/md_3.in -o out/{name}_box_md_3.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_2.rst -ref out/{name}_box_md_2.rst -r out/{name}_box_md_3.rst -x out/{name}_box_md_3.nc'
	check=sub(md3)
	endtime = datetime.datetime.now()
	print('md_3 complete')
	print (endtime - starttime)
	##############	md_3
if os.path.exists(f'out/{name}_box_md_4.rst')==0:
	print('run md_4 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md4=f'pmemd.cuda -O -i in/md_4.in -o out/{name}_box_md_4.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_3.rst -ref out/{name}_box_md_3.rst -r out/{name}_box_md_4.rst -x out/{name}_box_md_4.nc'
	check=sub(md4)
	endtime = datetime.datetime.now()
	print('md_4 complete')
	print (endtime - starttime)
	##############	md_4
if os.path.exists(f'out/{name}_box_md_5.rst')==0:
	print('run md_5 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md5=f'pmemd.cuda -O -i in/md_5.in -o out/{name}_box_md_5.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_4.rst -ref out/{name}_box_md_4.rst -r out/{name}_box_md_5.rst -x out/{name}_box_md_5.nc'
	check=sub(md5)
	endtime = datetime.datetime.now()
	print('md_5 complete')
	print (endtime - starttime)
	##############	md_5
if os.path.exists(f'out/{name}_box_md_6.rst')==0:
	print('run md_6 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md6=f'pmemd.cuda -O -i in/md_6.in -o out/{name}_box_md_6.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_5.rst -ref out/{name}_box_md_5.rst -r out/{name}_box_md_6.rst -x out/{name}_box_md_6.nc'
	check=sub(md6)
	endtime = datetime.datetime.now()
	print('md_6 complete')
	print (endtime - starttime)
	##############	md_6
if os.path.exists(f'out/{name}_box_md_7.rst')==0:
	print('run md_7 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md7=f'pmemd.cuda -O -i in/md_7.in -o out/{name}_box_md_7.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_6.rst -ref out/{name}_box_md_6.rst -r out/{name}_box_md_7.rst -x out/{name}_box_md_7.nc'
	check=sub(md7)
	endtime = datetime.datetime.now()
	print('md_7 complete')
	print (endtime - starttime)
	##############	md_7
if os.path.exists(f'out/{name}_box_md_8.rst')==0:
	print('run md_8 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md8=f'pmemd.cuda -O -i in/md_8.in -o out/{name}_box_md_8.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_7.rst -ref out/{name}_box_md_7.rst -r out/{name}_box_md_8.rst -x out/{name}_box_md_8.nc'
	check=sub(md8)
	endtime = datetime.datetime.now()
	print('md_8 complete')
	print (endtime - starttime)
	##############	md_8
if os.path.exists(f'out/{name}_box_md_9.rst')==0:
	print('run md_9 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md9=f'pmemd.cuda -O -i in/md_9.in -o out/{name}_box_md_9.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_8.rst -ref out/{name}_box_md_8.rst -r out/{name}_box_md_9.rst -x out/{name}_box_md_9.nc'
	check=sub(md9)
	endtime = datetime.datetime.now()
	print('md_9 complete')
	print (endtime - starttime)
	##############	md_9
if os.path.exists(f'out/{name}_box_md_10.rst')==0:
	print('run md_10 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md10=f'pmemd.cuda -O -i in/md_10.in -o out/{name}_box_md_10.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_9.rst -ref out/{name}_box_md_9.rst -r out/{name}_box_md_10.rst -x out/{name}_box_md_10.nc'
	check=sub(md10)
	endtime = datetime.datetime.now()
	print('md_10 complete')
	print (endtime - starttime)
	##############	md_10
if os.path.exists(f'out/{name}_box_md_11.rst')==0:
	print('run md_11 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md11=f'pmemd.cuda -O -i in/md_11.in -o out/{name}_box_md_11.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_10.rst -ref out/{name}_box_md_10.rst -r out/{name}_box_md_11.rst -x out/{name}_box_md_11.nc'
	check=sub(md11)
	endtime = datetime.datetime.now()
	print('md_11 complete')
	print (endtime - starttime)
	##############	md_11
if os.path.exists(f'out/{name}_box_md_12.rst')==0:
	print('run md_12 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md12=f'pmemd.cuda -O -i in/md_12.in -o out/{name}_box_md_12.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_11.rst -ref out/{name}_box_md_11.rst -r out/{name}_box_md_12.rst -x out/{name}_box_md_12.nc'
	check=sub(md12)
	endtime = datetime.datetime.now()
	print('md_12 complete')
	print (endtime - starttime)
	##############	md_12
if os.path.exists(f'out/{name}_box_md_13.rst')==0:
	print('run md_13 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md13=f'pmemd.cuda -O -i in/md_13.in -o out/{name}_box_md_13.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_12.rst -ref out/{name}_box_md_12.rst -r out/{name}_box_md_13.rst -x out/{name}_box_md_13.nc'
	check=sub(md13)
	endtime = datetime.datetime.now()
	print('md_13 complete')
	print (endtime - starttime)
	##############	md_13
if os.path.exists(f'out/{name}_box_md_14.rst')==0:
	print('run md_14 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md14=f'pmemd.cuda -O -i in/md_14.in -o out/{name}_box_md_14.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_13.rst -ref out/{name}_box_md_13.rst -r out/{name}_box_md_14.rst -x out/{name}_box_md_14.nc'
	check=sub(md14)
	endtime = datetime.datetime.now()
	print('md_14 complete')
	print (endtime - starttime)
	##############	md_14
if os.path.exists(f'out/{name}_box_md_15.rst')==0:
	print('run md_15 ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md15=f'pmemd.cuda -O -i in/md_15.in -o out/{name}_box_md_15.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_14.rst -ref out/{name}_box_md_14.rst -r out/{name}_box_md_15.rst -x out/{name}_box_md_15.nc'
	check=sub(md15)
	endtime = datetime.datetime.now()
	print('md_15 complete')
	print (endtime - starttime)
	##############	md_15
if os.path.exists(f'out/{name}_box_md.rst')==0:
	print('run md ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	md=f'pmemd.cuda -O -i in/md.in -o out/{name}_box_md.mdout -p in/{name}_box.prmtop -c out/{name}_box_md_15.rst -ref out/{name}_box_md_15.rst -r out/{name}_box_md.rst -x out/{name}_box_md.nc'
	check=sub(md)
	endtime = datetime.datetime.now()
	amb=f'ambpdb -p in/{name}_box.prmtop -c out/{name}_box_md.rst > out/{name}_box_md.pdb'
	sub(amb)
	print('md complete')
	print (endtime - starttime)
	##############	md
print('analyze')
open('in/analyze.cpptraj','w').write(f'parm in/{name}_box.prmtop\n'\
								  f'trajin out/{name}_box_md.nc\n'\
								  f'autoimage :1-{order}\n'\
								  f'strip :WAT\n'\
								  f'rms first\n'\
								  f'rms ToFirst :1-{order}&!@H= first out out/{name}_rmsd.agr mass\n'\
								  f'average crdset MyAvg :1-{order}\n'\
								  f'rms ref MyAvg\n'\
								  f'rmsf byres out out/{name}_rmsf.agr :1-{order}\n'\
								  f'run')
ana=f'cpptraj in/analyze.cpptraj'
sub(ana)
if amd==1:
	with open(f'out/{name}_box_md.mdout','r') as mdout:
	 	for line in mdout:
			 if re_search('A V E R A G E S   O V E R', line) != None:
	 			nullline1 = next(mdout)
	 			nullline2 = next(mdout)
	 			NSTEPline = next(mdout)
	 			Etotline = next(mdout)
	 			BONDline = next(mdout)
	 			UBline = next(mdout)
	Average_Dihedral=float(BONDline.split()[8])
	Average_EPtot=float(Etotline.split()[8])
	total_atoms=float(atoms)
	protein_residues=float(order)
	Approximate_energy_contribution_per_degree_of_freedom=float(protein_residues*4)
	print(Average_Dihedral,Average_EPtot,total_atoms,protein_residues,Approximate_energy_contribution_per_degree_of_freedom)
	ethreshd=format(Approximate_energy_contribution_per_degree_of_freedom+Average_Dihedral,'.4f')
	alphad=format(Approximate_energy_contribution_per_degree_of_freedom*0.2,'.4f')
	alphap=format(total_atoms*0.2,'.4f')
	ethreshp=format(Average_EPtot+float(alphap),'.4f')
	open('in/amd.in','w').write(f'explicit solvent production run\n'\
	 						   f'&cntrl\n'\
	 						   f'  imin=0,\n'\
	 						   f'  irest=1,\n'\
	 						   f'  ntx=5,\n'\
	 						   f'  nstlim=25000000,\n'\
	 						   f'  dt=0.002,\n'\
	 						   f'  ntc=2,\n'\
	 						   f'  ntf=2,\n'\
	 						   f'  cut=12.0,\n'\
	 						   f'  ntb=2,\n'\
	 						   f'  ntp=1,\n'\
	 						   f'  taup=2.0,\n'\
	 						   f'  ntpr=5000,\n'\
	 						   f'  ntwx=5000,\n'\
	 						   f'  ntwr=50000,\n'\
	 						   f'  ntt=3,\n'\
	 						   f'  gamma_ln=2.0,\n'\
	 						   f'  temp0=300.0,\n'\
	 						   f'  ig=-1,\n'\
	 						   f'  iwrap=1\n'\
	 						   f'  iamd=3,\n'\
	 						   f'  ethreshd={ethreshd}\n'\
	 						   f'  alphad={alphad}\n'\
	 						   f'  alphap={alphap}\n'\
	 						   f'  ethreshp={ethreshp}\n'\
	 						   f'  / \n END')
	##############	amd
	print('run amd ... waiting\nmay time-consuming\n.....')
	starttime = datetime.datetime.now()
	amd=f'pmemd.cuda -O -i in/amd.in -o out/{name}_box_amd.mdout -p in/{name}_box.prmtop -c out/{name}_box_md.rst -ref out/{name}_box_md.rst -r out/{name}_box_amd.rst -x out/{name}_box_amd.nc'
	check=sub(amd)
	endtime = datetime.datetime.now()
	print('amd complete')
	print (endtime - starttime)
	##############	amd
	open('in/analyze_amd.cpptraj','w').write(f'parm in/{name}_box.prmtop\n'\
								  f'trajin out/{name}_box_amd.nc\n'\
								  f'autoimage :1-{order}\n'\
								  f'strip :WAT\n'\
								  f'rms first\n'\
								  f'rms ToFirst :1-{order}&!@H= first out out/{name}_rmsd_amd.agr mass\n'\
								  f'average crdset MyAvg :1-{order}\n'\
								  f'rms ref MyAvg\n'\
								  f'rmsf byres out out/{name}_rmsf_amd.agr :1-{order}\n'\
								  f'run')
	amdana=f'cpptraj in/analyze_amd.cpptraj'
	sub(amdana)
print('analyze complete\nall program done')

```
