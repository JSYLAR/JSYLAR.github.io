```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Initialise ChemShell
from chemsh import *
from chemsh.io import file

# Parse charges from AMBER prmtop
prmtop = file.parse('T5M_box.prmtop', fmt='amber_prmtop')
for key, val in prmtop.items():
    if type(val) is dict and 'atom' in val:
        charges = prmtop[key]['atom']['data']['charge']
# Import coords from xyz file and charges from prmtop
my_mol = Fragment(coords='REA.xyz',charges=charges)
my_pdb = Fragment(coords='T5M_box.pdb',charges=charges)
haem = list(range(8089,8163))
lig = list(range(8037,8089))
cym = list(range(7156,7160))
# Concatenate the lists to form the QM region
qm_region = haem + cym + lig
# Save for viewing
frag_qm_region = my_mol.getSelected(qm_region)
frag_qm_region.save('qm_region.xyz')
# Select activate region
active_region = my_pdb.selectByShell(around=qm_region, convex=True, padding=10.0, unit='a.u.', boundary='inclusive', return_masks=False)
# Save for viewing
frag_active_region = my_mol.getSelected(active_region)
frag_active_region.save('active_region.xyz')
# Define QM method
my_qm =ORCA(functional="PBE0", basis="def2-SVP",d4=True,convergence="TightSCF",nprocs='24',charge='-2', mult='2', scftype='uhf',restart=False,auxbasis='def2/J',exchange="RIJCOSX")
# Define the MM method (DL_POLY)
my_mm = DL_POLY(ff='T5M_box.prmtop', rcut=99.99)
# Define the QM/MM calculation
my_qmmm = QMMM(frag=my_mol, mm=my_mm, qm=my_qm, qm_region=qm_region, embedding="electrostatic")
# Run QM/MM geometry optimisation with DL-FIND
my_opt = Opt(theory=my_qmmm, active=active_region, algorithm="lbfgs", maxcycle=1000, maxene=2000)
my_opt.run()
#opt = Opt(theory=my_theory, dimer=True, coordinates="dlc", algorithm="lbfgs",delta=0.01, tolerance=0.0003, trustradius="const")
```
