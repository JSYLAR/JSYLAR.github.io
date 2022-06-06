```
# Single-point QM/MM calculation on the P450 system
#
# Created by YL Jul 2021
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Initialise ChemShell
from chemsh import *
from chemsh.io import file
import numpy as np

# Parse charges from AMBER prmtop
prmtop = file.parse('82D_box.prmtop', fmt='amber_prmtop')
for key, val in prmtop.items():
    if type(val) is dict and 'atom' in val:
        charges = prmtop[key]['atom']['data']['charge']
# Import coords from xyz file and charges from prmtop
my_mol_1 = Fragment(coords='REA.xyz',charges=charges)
# Import coords from pdb file and charges from prmtop
my_pdb = Fragment(coords='82D_box.pdb',charges=charges)
# Select QM region based on pdb file
haem = list(range(7955,8016))+[8028]
lig = my_pdb.select(residues=['AGI'], side_chain=True).tolist()
cym = list(range(7034,7038))
h2o = [8523,8524,8525]
# Concatenate the lists to form the QM region
qm_region = haem + cym + lig + h2o
# Save for viewing
frag_qm_region = my_mol_1.getSelected(qm_region)
frag_qm_region.save('qm_region.xyz')
# Select activate region based on pdb file
active_region = my_pdb.selectByShell(around=qm_region, convex=True, padding=8.0, unit='a.u.', boundary='inclusive', return_masks=False)
# Save for viewing
frag_active_region = my_mol_1.getSelected(active_region)
frag_active_region.save('active_region.xyz')
# Define QM method
my_qm =ORCA(functional='b3lyp', convergence='TightSCF',basis='def2-SVP',auxbasis='def2/J',exchange='RIJCOSX',d4=True,nprocs='48',charge='0',CHF='0.15', mult='2',scftype='uhf',soscf=True)
#my_qm =ORCA(functional="r2scan-3c", convergence="TightSCF",basis="def2-SVP",exchange="RIJCOSX",auxbasis="def2/J",d4=True,nprocs='48',charge='0', mult='2',scftype='uhf',soscf=True)
#my_qm =ORCA(functional="r2scan-3c", convergence="TightSCF",nprocs='48',charge='0', mult='2',scftype='uhf',soscf=True)
# Define the MM method (DL_POLY)
my_mm = DL_POLY(ff='82D_box.prmtop', rcut=99.99)
# Define the QM/MM calculation
my_qmmm = QMMM(frag=my_mol_1, mm=my_mm, qm=my_qm, qm_region=qm_region, embedding="electrostatic")
my_sp = SP(theory=my_qmmm)
my_sp.run()
```
