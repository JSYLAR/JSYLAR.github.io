```
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 16:10:22 2021

@author: baijie
"""
import sys,getopt,os,datetime,subprocess
def usage():										      ### help documents
	useinfo = '''
	-h:\thelp documents.\n
	-i:\tinput pdb file name like <1AB2>.\n
	-j:\tthreads like <3>.\n
	-m:\tchose sander or pmemd \n
	-u:\tuse cuda like <cuda>
	-n:\t
	'''
	print (useinfo)
	exit()
opts,args = getopt.getopt(sys.argv[1:],'hi:m:j:u:n:')
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
	elif op == '-h':
		usage()
name = targetfile
print(name)
with open('in/'+name+'_box.pdb','r') as seqread:
	line = seqread.readlines()
	for lines in line:
		li = lines.split()
		try:
			if ('OXT') in li:
				seqR=(lines.split('OXT')[1].split()[1])
			elif ('Na+') in li:
				seqC=(lines.split('Na+')[2].split()[0])
				break
			elif ('Cl-') in li:
				seqC=(lines.split('Cl-')[2].split()[0])
			elif ('WAT') in li:
				seqC=(lines.split('WAT')[1].split()[0])
				break
		except:
			continue
order=str(seqR)
corder=str(int(seqC)-1)
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
							 f'  nstlim=250000,\n'\
							 f'  dt=0.0005,\n'\
							 f'  ntc=2,\n'\
							 f'  ntf=2,\n'\
							 f'  ntx=1,\n'\
							 f'  cut=8.0,\n'\
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
open('in/press.in','w').write(f'explicit solvent density: 50ps\n'\
								f' &cntrl\n'\
								f'  imin=0,\n'\
								f'  irest=1,\n'\
								f'  ntx=5,\n'\
								f'  nstlim=250000,\n'\
								f'  dt=0.0001,\n'\
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
							 f'  ntwr=50000,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  nstlim=2500000,\n'\
						   f'  dt=0.002,\n'\
						   f'  ntc=2,\n'\
						   f'  ntf=2,\n'\
						   f'  cut=8.0,\n'\
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
						   f'  cut=8.0,\n'\
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
print('run min1 ... waiting\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/min1.in -o out/'+name+'_box_min1.mdout -p in/'+name+'_box.prmtop -c in/'+name+'_box.inpcrd -r out/'+name+'_box_min1.rst -ref in/'+name+'_box.inpcrd',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
subprocess.run('ambpdb -p in/'+name+'_box.prmtop -c out/'+name+'_box_min1.rst > out/'+name+'_box_min1.pdb',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('mining1 complete')
print (endtime - starttime)
###############	min1
print('run min2 ... waiting\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/min2.in -o out/'+name+'_box_min2.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_min1.rst -r out/'+name+'_box_min2.rst -ref out/'+name+'_box_min1.rst',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
subprocess.run('ambpdb -p in/'+name+'_box.prmtop -c out/'+name+'_box_min2.rst > out/'+name+'_box_min2.pdb',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('mining1 complete')
print (endtime - starttime)
###############	min2
print('run heat ... waiting\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/heat.in -o out/'+name+'_box_heat.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_min2.rst -r out/'+name+'_box_heat.rst -x out/'+name+'_box_heat.nc -ref out/'+name+'_box_min2.rst',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
subprocess.run('ambpdb -p in/'+name+'_box.prmtop -c out/'+name+'_box_heat.rst > out/'+name+'_box_heat.pdb',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('heating complete')
print (endtime - starttime)
##############	heat
print('run press ... waiting\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/press.in -o out/'+name+'_box_press.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_heat.rst -r out/'+name+'_box_press.rst -x out/'+name+'_box_press.nc -ref out/'+name+'_box_heat.rst',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
subprocess.run('ambpdb -p in/'+name+'_box.prmtop -c out/'+name+'_box_press.rst > out/'+name+'_box_press.pdb',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('pressing complete')
print (endtime - starttime)
##############	press
print('run eq ... waiting\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/eq.in -o out/'+name+'_box_eq.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_press.rst -ref out/'+name+'_box_press.rst -r out/'+name+'_box_eq.rst -x out/'+name+'_box_eq.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
subprocess.run('ambpdb -p in/'+name+'_box.prmtop -c out/'+name+'_box_eq.rst > out/'+name+'_box_eq.pdb',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('eq complete')
print (endtime - starttime)
##############	eq
print('run md_1 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_1.in -o out/'+name+'_box_md_1.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_eq.rst -ref out/'+name+'_box_eq.rst -r out/'+name+'_box_md_1.rst -x out/'+name+'_box_md_1.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_1 complete')
print (endtime - starttime)
##############	md_1
print('run md_2 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_2.in -o out/'+name+'_box_md_2.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_1.rst -ref out/'+name+'_box_md_1.rst -r out/'+name+'_box_md_2.rst -x out/'+name+'_box_md_2.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_2 complete')
print (endtime - starttime)
##############	md_2
print('run md_3 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_3.in -o out/'+name+'_box_md_3.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_2.rst -ref out/'+name+'_box_md_2.rst -r out/'+name+'_box_md_3.rst -x out/'+name+'_box_md_3.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_3 complete')
print (endtime - starttime)
##############	md_3
print('run md_4 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_4.in -o out/'+name+'_box_md_4.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_3.rst -ref out/'+name+'_box_md_3.rst -r out/'+name+'_box_md_4.rst -x out/'+name+'_box_md_4.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_4 complete')
print (endtime - starttime)
##############	md_4
print('run md_5 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_5.in -o out/'+name+'_box_md_5.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_4.rst -ref out/'+name+'_box_md_4.rst -r out/'+name+'_box_md_5.rst -x out/'+name+'_box_md_5.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_5 complete')
print (endtime - starttime)
##############	md_5
print('run md_6 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_6.in -o out/'+name+'_box_md_6.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_5.rst -ref out/'+name+'_box_md_5.rst -r out/'+name+'_box_md_6.rst -x out/'+name+'_box_md_6.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_6 complete')
print (endtime - starttime)
##############	md_6
print('run md_7 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_7.in -o out/'+name+'_box_md_7.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_6.rst -ref out/'+name+'_box_md_6.rst -r out/'+name+'_box_md_7.rst -x out/'+name+'_box_md_7.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_7 complete')
print (endtime - starttime)
##############	md_7
print('run md_8 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_8.in -o out/'+name+'_box_md_8.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_7.rst -ref out/'+name+'_box_md_7.rst -r out/'+name+'_box_md_8.rst -x out/'+name+'_box_md_8.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_8 complete')
print (endtime - starttime)
##############	md_8
print('run md_9 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_9.in -o out/'+name+'_box_md_9.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_8.rst -ref out/'+name+'_box_md_8.rst -r out/'+name+'_box_md_9.rst -x out/'+name+'_box_md_9.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_9 complete')
print (endtime - starttime)
##############	md_9
print('run md_10 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_10.in -o out/'+name+'_box_md_10.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_9.rst -ref out/'+name+'_box_md_9.rst -r out/'+name+'_box_md_10.rst -x out/'+name+'_box_md_10.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_10 complete')
print (endtime - starttime)
##############	md_10
print('run md_10 ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_11.in -o out/'+name+'_box_md_11.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_10.rst -ref out/'+name+'_box_md_10.rst -r out/'+name+'_box_md_11.rst -x out/'+name+'_box_md_11.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_11 complete')
print (endtime - starttime)
##############	md_11
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_12.in -o out/'+name+'_box_md_12.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_11.rst -ref out/'+name+'_box_md_11.rst -r out/'+name+'_box_md_12.rst -x out/'+name+'_box_md_12.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_12 complete')
print (endtime - starttime)
##############	md_12
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_13.in -o out/'+name+'_box_md_13.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_12.rst -ref out/'+name+'_box_md_12.rst -r out/'+name+'_box_md_13.rst -x out/'+name+'_box_md_13.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_13 complete')
print (endtime - starttime)
##############	md_13
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_14.in -o out/'+name+'_box_md_14.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_13.rst -ref out/'+name+'_box_md_13.rst -r out/'+name+'_box_md_14.rst -x out/'+name+'_box_md_14.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_14 complete')
print (endtime - starttime)
##############	md_14
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md_15.in -o out/'+name+'_box_md_15.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_14.rst -ref out/'+name+'_box_md_14.rst -r out/'+name+'_box_md_15.rst -x out/'+name+'_box_md_15.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
print('md_15 complete')
print (endtime - starttime)
##############	md_15
print('run md ... waiting\nmay time-consuming\n.....')
starttime = datetime.datetime.now()
subprocess.run(threads+proce+GPU+mpi+' -O -i in/md.in -o out/'+name+'_box_md.mdout -p in/'+name+'_box.prmtop -c out/'+name+'_box_md_15.rst -ref out/'+name+'_box_md_15.rst -r out/'+name+'_box_md.rst -x out/'+name+'_box_md.nc',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
endtime = datetime.datetime.now()
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
subprocess.run('cpptraj in/analyze.cpptraj',stdin=None, input=None, stdout=None, stderr=None, timeout=None, check=False, universal_newlines=False,shell=True)
print('analyze complete\nall program done')
```
