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
my_mol_1 = Fragment(coords='dimer1.xyz',charges=charges)
my_mol_2 = Fragment(coords='dimer2.xyz',charges=charges)
# Import coords from pdb file and charges from prmtop
my_pdb = Fragment(coords='T5M_box.pdb',charges=charges)
# Select QM region based on pdb file
haem = list(range(8089,8150))+[8162]
lig = my_pdb.select(residues=['TAX'], side_chain=True).tolist()
cym = [7156,7157,7158,7159]
# Concatenate the lists to form the QM region
qm_region = haem + cym + lig
# Save for viewing
frag_qm_region = my_mol_1.getSelected(qm_region)
frag_qm_region.save('qm_region.xyz')
# Select activate region based on pdb file
active_region = my_pdb.selectByShell(around=qm_region, convex=True, padding=10.0, unit='a.u.', boundary='inclusive', return_masks=False)
# Save for viewing
frag_active_region = my_mol_1.getSelected(active_region)
frag_active_region.save('active_region.xyz')
# Define QM method
#my_qm =ORCA(functional="r2scan-3c", convergence="TightSCF",basis="def2-SVP",exchange="RIJCOSX",auxbasis="def2/J",d4=True,nprocs='48',charge='0', mult='2',scftype='uhf',soscf=True)
my_qm =ORCA(functional="r2scan-3c", convergence="TightSCF",nprocs='48',charge='0', mult='2',scftype='uhf',soscf=True)
# Define the MM method (DL_POLY)
my_mm = DL_POLY(ff='T5M_box.prmtop', rcut=99.99)
# Define the QM/MM calculation
my_qmmm = QMMM(frag=my_mol_1, mm=my_mm, qm=my_qm, qm_region=qm_region, embedding="electrostatic")
# Run QM/MM geometry optimisation with DL-FIND
#my_opt = Opt(theory=my_qmmm, active=active_region, algorithm="lbfgs", maxcycle=1000, maxene=2000)
#my_opt = Opt(theory=my_qmmm, frag2=my_mol_2, dimer=True, delta=0.1ï¼Œalgorithm="lbfgs", maxcycle=1000, maxene=2000, trust_radius="const")
my_opt = Opt(theory=my_qmmm, dimer=True, delta=0.1ï¼Œalgorithm="lbfgs", maxcycle=1000, maxene=2000ï¼Œtrust_radius="const")
my_opt.run()
my_mol_1.save("dimer_opt.xyz")
```
