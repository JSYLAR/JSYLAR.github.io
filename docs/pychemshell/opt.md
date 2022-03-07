```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Initialise ChemShell
from chemsh import *
from chemsh.io import file
import numpy as np

# Parse charges from AMBER prmtop
prmtop = file.parse('T5M_box.prmtop', fmt='amber_prmtop')
for key, val in prmtop.items():
    if type(val) is dict and 'atom' in val:
        charges = prmtop[key]['atom']['data']['charge']
# Import coords from xyz file and charges from prmtop
my_mol = Fragment(coords='REA.xyz',charges=charges)
# Import coords from pdb file and charges from prmtop
my_pdb = Fragment(coords='T5M_box.pdb',charges=charges)
# Select QM region based on pdb file
haem = list(range(8089,8150))+[8162]
lig = my_pdb.select(residues=['TAX'], side_chain=True).tolist()
cym = [7156,7157,7158,7159]
h2o = [8289,8290,8291]
# Concatenate the lists to form the QM region
qm_region = haem + cym + lig + h2o
# Save for viewing
frag_qm_region = my_mol.getSelected(qm_region)
frag_qm_region.save('qm_region.xyz')
# Select activate region based on pdb file
active_region = my_pdb.selectByShell(around=qm_region, convex=True, padding=8.0, unit='a.u.', boundary='inclusive', return_masks=False)
# Save for viewing
frag_active_region = my_mol.getSelected(active_region)
frag_active_region.save('active_region.xyz')
# Define QM method
my_qm =ORCA(functional='PBE0', convergence='TightSCF',basis='def2-SVP',auxbasis='def2/J',exchange='RIJCOSX',d4=True,nprocs='48',charge='0',broken='2,1', mult='2',scftype='uhf',soscf=True)
#my_qm =ORCA(functional="bp86", convergence="TightSCF",basis="def2-SVP",d4=True,nprocs='48',charge='0', mult='2',scftype='uhf',soscf=True)
#my_qm =ORCA(functional="r2scan-3c", convergence="TightSCF",nprocs='48',charge='0', mult='2',scftype='uhf',soscf=True)
# Define the MM method (DL_POLY)
my_mm = DL_POLY(ff='T5M_box.prmtop', rcut=99.99)
# Define the QM/MM calculation
my_qmmm = QMMM(frag=my_mol, mm=my_mm, qm=my_qm, qm_region=qm_region, embedding="electrostatic")
# Run QM/MM geometry optimisation with DL-FIND
my_opt = Opt(theory=my_qmmm, active=active_region, algorithm="lbfgs", maxcycle=1000, maxene=1000,save_path=True)
my_opt.run()
my_mol.save('REA_OPT.xyz')
```
