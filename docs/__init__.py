#  Copyright (C) 2018 The authors of Py-ChemShell
#
#  This file is part of Py-ChemShell.
#
#  Py-ChemShell is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  Py-ChemShell is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with Py-ChemShell.  If not, see
#  <http://www.gnu.org/licenses/>.

# david.gunn@stfc.ac.uk

import re
import os.path
import math
from numpy         import full, zeros
from ...base       import errors
from ...utils      import fileutils
from ..qm          import _QM
from ...data       import atomicdata, unitconvert

class ORCA(_QM):
    '''Interface to ORCA'''

    _attrs = {
               'auxbasis'              :'',
               'basisspec'             : False,
               # YL 09/03/2021: (suggested by HMS) with ORCA it's always encouraged to use "TightSCF" although "NormalSCF" is the default
               # YL NB 09/03/2021: but we may change the option's keyword in the future to make it uniform for all interfaces (currently other interfaces use "threshold=1.0e-6")
               'convergence'           :"TightSCF",
               'slowconv'              : False,
               'exchange'              : "",
               'CHF'                   : "",
               'soscf'                 : False,
               'cosmo'                 : None,
               'd3'                    : False,
               'd4'                    : False,
               'enerflag'              : 1,
               'energy_correction'     : 0.0,
               'eroots'                : 1,
               'estate'                : 1,
               'excited'               : False,
               'explicit'              : False,
               'exp_list'              : [],
               'guess'                 : "PAtom",
               'image'                 : None,
               'input'                 :"_orca.inp",
               'jobname'               :"_orca",
               'list_option'           : "medium",
               'listing_index'         : 1,
               'moinp'                 : "save.gbw",
               'newgto'                : None,
               'nprocs'                : 1,
               'num_explicit'          : 0,
               'CPU'                   : False ,
               'old_moinp'             :"_orca.gbw",
               'optstr'                :'',
               'output'                :"_orca.out",
               'output_bqs'            :"_orca.pcgrad",
               'output_eandg'          :"_orca.engrad",
			   'qm_atom'               :'',
			   'orca_parmtop'          :'',
			   'qmmm'                  :False,
               'path'                  : '/home/baij/soft/orca_5_0_3_linux_x86-64_shared_openmpi411/orca',
                # v4.0 changed some basis set input conventions
               'version'               : 4.0,
             }

    _internals = {
                   '_basis_element' : [],
                   '_basis_list'    : '',
                   '_basis_sym'     : [],
                   '_ecp_list'      : '',
                   '_ecp_ncore'     : [],
                   '_ecp_sym'       : [],
                   '_exec_run_shell': True,
                   '_syscmd'        : 'orca',
                 }

    _synons = {
                'blyp' : 'becke88 lyp',
                'lda'  : 'slater vwn_5',
                's-vwn': 'slater vwn_5',
                'hf'   : 'hf',
                'dft'  : 'dft'
              }

    def getInpBuff(self):
        '''String buff containing the input information'''

        if self.frag.bqs:
            self.frag.nbqs = len(self.frag.bqs.coords)
            ncent = self.frag.natoms + self.frag.nbqs

        method = self._synons.get(self.method.lower())
        self.hamout = method

        strbuff = '#ORCA input file generated by ChemShell\n'
        strbuff += "! QMMM \n"
        strbuff += "! %s \n" % (self.functional)
		
        if self.d3:
             strbuff += " D3"
        if self.d4:
             strbuff += "! D4 \n"
        strbuff += "! %s \n" % (self.convergence)
        if self.exchange:
             strbuff += "! %s \n" % (self.exchange)
        if self.slowconv:
             strbuff += "! slowconv NoTrah\n"
        if self.soscf:
             strbuff += "! soscf NoTrah slowconv\n"
        if self.cosmo:
             strbuff += "! COSMO(%s)\n" % (self.cosmo)
        strbuff += "! defgrid2\n"

        #Parallel execution
        if self.nprocs > 1:
            strbuff += "%pal\n"
            strbuff += "  nprocs %s\n" % (self.nprocs)
            strbuff += "end\n"
        strbuff += "%maxcore 2000\n"

        #Specify the point charge file
        if self.frag.nbqs > 0:
            strbuff += "%pointcharges \"pointcharges.xyz\" \n"

        #Method
        strbuff += "%method\n"
        if self.CHF:
            strbuff += "  ACM %s\n" % (self.CHF)
        if self.enerflag:
            if self._gradients:
                strbuff += "  RunTyp Gradient\n"
            else:
                strbuff += "  RunTyp Energy\n"
        #strbuff += "  FrozenCore FC_ELECTRONS\n"
        strbuff += "end\n"

        #Basis set
#         Determine if self.basis contains one or more basis, or if file type with newGTO info
#         Individual newGTO Basis info written after the atom in the 'coords' section
        if self.basis:
         words = self.basis.split()
#         case 1: one item in self.basis with global basis info 
         if (len(words) == 1):
          strbuff += "%basis\n"
          if self.version < 4.0:
            strbuff += "  Basis %s\n" % (self.basis)
          else:
            strbuff += "  Basis \"%s\" \n" % (self.basis)
	          #Auxiliary basis for RI method
          if self.auxbasis:
            if self.version < 4.0:
                strbuff += "  Aux %s\n" % (self.auxbasis)
            else:
                strbuff += "  Aux \"%s\" \n" % (self.auxbasis)
          strbuff += "end\n"
#         case 2: more than one item in self.basis but not read in from file
         if (len(words) > 1) and "\"" not in self.basis.lower():
          strbuff += "%basis\n"
          strbuff += "  %s\n" % (self.basis)
          if self.auxbasis:
            if self.version < 4.0:
                strbuff += "  Aux %s\n" % (self.auxbasis)
            else:
                strbuff += "  Aux \"%s\" \n" % (self.auxbasis)
          strbuff += "end\n"
#         case 3: basis set in file
         if (len(words) > 1) and "\"" in self.basis.lower():
          self.basisspec = True
          lines = self.basis.splitlines()
          num_basis = 0
          self._basis_sym = [None] * (self.frag.natoms+1) 
          self._basis_element = [None] * (self.frag.natoms+1)
          self._basis_list = [None] * (self.frag.natoms+1)
          for line in lines:
            if "\"" in line:
              num_basis += 1
              word = line.split("\"")
              self._basis_sym[num_basis] = word[1]
              self._basis_element[num_basis] = ''.join([k for k in word[1] if not k.isdigit()])
              self._basis_list[num_basis] = "newGTO \n"
            else:
              if (num_basis > 0):
                if ("newgto" not in line.lower()):
                    self._basis_list[num_basis] +="%s" % (line.rstrip())
                if ("end" not in line.lower()):
                    self._basis_list[num_basis] +="\n"
                
        #ECPs
        if self.ecp:
            num_ecp = 0
            j = ''
            self._ecp_ncore = [None] * (self.frag.natoms+1)
            self._ecp_sym = [None] * (self.frag.natoms+1)
            self._ecp_list = [None] * (self.frag.natoms+1)
            if os.path.isfile(os.path.abspath(self.ecp)):
#               ECP is in a file
                ecp_list = fileutils.file2text(self.ecp)
                lines = ecp_list.splitlines()
                for line in lines:
                  if "\"" in line:
                    num_ecp += 1
                    word = line.split("\"")
                    self._ecp_sym[num_ecp] = word[1]
                    j.join([k for k in word[1] if not k.isdigit()])
                    self._ecp_list[num_ecp] = "NewECP \n"
                  else:
                    if ("newecp" not in line.lower()):
                      self._ecp_list[num_ecp] +="%s\n" % (line)
                  if "core" in line.lower():
                    word = line.split()
                    self._ecp_ncore[num_ecp] = word[1]
            else:
#               ECP was defined in the input script
                lines = self.ecp.splitlines()
                for line in lines:
                    strbuff += line + '\n'
                    if "\"" in line:
                      num_ecp += 1
                      word = line.split("\"")
                      self._ecp_sym[num_ecp] = word[1]
                      j.join([k for k in word[1] if not k.isdigit()])
                      self._ecp_list[num_ecp] = "NewECP \n"
                    else:
                      if ("newecp" not in line.lower()):
                        self._ecp_list[num_ecp] +="%s\n" % (line)
                    if "core" in line.lower():
                      word = line.split()
                      self._ecp_ncore[num_ecp] = word[1]

        #SCF control
        strbuff += "%scf\n"
        strbuff += "  DirectResetFreq 1\n"
        strbuff += "  DIIS Start 0.1 MaxIt 5 MaxEq 20 BFac 1.2 MaxC 15.0 end \n"
        strbuff += "  SOSCFStart 0.0001 \n"
        #strbuff += "  DampErr 0.001 \n"
        strbuff += "  HFTyp %s\n" % (self.scftype)
        if self.restart:
            fileutils.rename(self.old_moinp,self.moinp)
            strbuff += "  Guess MORead\n"
            #strbuff += "  MOInp \"%s\" \n" % (self.moinp)
            strbuff += "  MOInp \"save.gbw\" \n"
        else:
#           Patom and Pmodel seem to fail when defining own Basis or ECP so defaulting to hueckel
            if self.guess:
                strbuff += f'  Guess {self.guess}\n'
            strbuff += "  AutoStart false\n"
            if self.broken:
                strbuff += f'  BrokenSym {self.broken}\n'
    
        if self.direct:
            strbuff += "  SCFMode Direct\n"
        else:
            strbuff += "  SCFMode Conventional\n"
    
        if self.maxiter:
            strbuff += "  MaxIter %s\n" % (self.maxiter)
    
        strbuff += "end\n"

        #Excited states
        if self.excited:
            if self.hamout == 'hf':
                strbuff += "%cis\n"
            elif self.hamout == 'dft':
                strbuff += "%tddft\n"
        
            # Must calculate as least as many roots as the state of interest
            if self.eroots > self.estate:
                strbuff += "  NRoots %s\n" % (self.eroots)
            else:
                strbuff += "  NRoots %s\n" % (self.estate)
            strbuff += "  IRoot %s\n" % (self.estate)
            strbuff += "end\n"
        if self.qmmm:
	        strbuff += "%qmmm\n"
	        strbuff += "QMAtoms {%s} end\n" % (self.qm_atom)
	        strbuff += 'ORCAFFFilename "%s"\nend\n'% (self.orca_parmtop)
			
        #Geometry
        strbuff += "%coords\n"
        strbuff += "  CTyp xyz\n"
        strbuff += "  Mult %s\n" % (self.mult)
        strbuff += "  Units bohrs\n"
        strbuff += "  coords\n"

        #Point charge file
        if self.frag.nbqs:

            fp = open('pointcharges.xyz', 'w+')
            self.num_explicit = 0
            self.exp_list.clear() 
            num_file_bqs = 0
            ecprange = self.frag.bqs.getRegion(2)
            for i in range(self.frag.bqs.nbqs): 
#               This initial loop is to determine the number of bqs to be written in the pointcharges file, and removes the pointcharge(s)
#               that have to be treated differently (i.e. when requiring an 'explicit' interface)
                name = str(self.frag.bqs.names[i])
#               There's probably a neater way to strip the extraneous bits from the name but it'll do in a pinch
                name = name.replace(' ','')
                name = name.replace('\'','')
                name = name.replace('b','')
                coords = list(self.frag.bqs.coords[i])
                if (name not in self._ecp_sym):
                  num_file_bqs += 1
            fp.write(str(num_file_bqs))
            fp.write('\n')
            for i in range(self.frag.bqs.nbqs):
#               This loop writes the bq info into the pointcharges file.
                name = str(self.frag.bqs.names[i])
                name = name.replace(' ','')
                name = name.replace('\'','')
                name = name.replace('b','')
                coords = list(self.frag.bqs.coords[i])
                if (name not in self._ecp_sym):
#               Not an explicit ECP - added to pointcharges file
                  for j in range(3):
                      coords[j] = coords[j] / unitconvert.Angstrom2Bohr
                  fp.write('{0:3.10f} {1:3.10f} {2:3.10f} {3:3.10f}\n'.format(self.frag.bqs.charges[i], coords[0], coords[1], coords[2]))
                else:
#               Explicit ECP - added to main input file
                  element = '' 
                  element = element.join([k for k in name if not k.isdigit()])
                  atom_charge = self.frag.bqs.charges[i]
                  self.explicit = True
                  self.num_explicit += 1
                  self.exp_list.append(i)
                  strbuff += "%s> %s %s %s %s " % (element, atom_charge, coords[0], coords[1], coords[2])
                  for j in range(1,num_ecp+1):
                    if name in self._ecp_sym[j]:
                      strbuff += "\n%s" % (self._ecp_list[j])
            fp.close()

#           Due to the way the explicit ECPs are treated we need to remove the coulombic interaction between the explicit ECPs and the 
#           remaining bqs.
            self.energy_correction = 0.0
            test_e = 0.0
            for i in self.exp_list:
                coords_i = list(self.frag.bqs.coords[i])
                for j in range(self.frag.bqs.nbqs):
                  dist = 0.0
                  chargeprod = 0.0
                  coords_j = list(self.frag.bqs.coords[j])
                  chargeprod=-1.0 * self.frag.bqs.charges[i] * self.frag.bqs.charges[j]
                  for k in range(3):
                    dist += (coords_i[k] - coords_j[k])**2
                  dist = math.sqrt(dist) 
                  if dist and chargeprod:
                    if (j in self.exp_list) and (j > i):
                      test_e += chargeprod/dist
                    if j not in self.exp_list:
                      self.energy_correction += chargeprod / dist
            self.energy_correction += test_e

        for i in range(self.frag.natoms):
            coords = list(self.frag.coords[i])
            symbol = self.frag.names[i].decode('utf-8')#str(atomicdata.symbols[self.frag.znums[i]])
            element = str(atomicdata.symbols[self.frag.znums[i]])
#           Here we are checking if each element has an ECP, BASIS, both or neither and adding the appropriate info to strbuff
#           We need the differentiation as if ECP-only (treating as embedded shell) then the formatting is different
#           ORCA doesn't understand numbers after the element, so individual atom identification (for ECP and Basis assignment)
#           happens in the background with the 'symbol' variable.
            if self.ecp:
              shell_only = True 
              basis_only = True
              for j in range(1,num_ecp+1):
                if symbol in self._ecp_sym[j]:
                  basis_only = False
              if basis_only:
                strbuff += "%s %s %s %s " % (element, coords[0], coords[1], coords[2])
              else:
                if self.basisspec:
                  for k in range (1,num_basis+1):
                    if symbol in self._basis_sym[k]:
                      shell_only = False
                  if shell_only: #ECP only found for this atom (Implicit interface)
                      for j in range(1,num_ecp+1):
                        if symbol in self._ecp_sym[j]:
                            atom_charge = self.frag.znums[i] - int(self._ecp_ncore[j])
                            strbuff += "%s> %s %s %s %s " % (element, atom_charge, coords[0], coords[1], coords[2])
                  else: #ECPs used and basis found for this atom
                    strbuff += "%s %s %s %s " % (element, coords[0], coords[1], coords[2])
                else: #ECPs used but global basis used therefore not shell only
                  strbuff += "%s %s %s %s " % (element, coords[0], coords[1], coords[2])
            else: 
              strbuff += "%s %s %s %s " % (element, coords[0], coords[1], coords[2])
            if self.basisspec:
              for j in range(1,num_basis+1):
                if symbol in self._basis_sym[j]:
                  strbuff += "\n%s" % (self._basis_list[j])
            if self.ecp:
              for j in range(1,num_ecp+1):
                if symbol in self._ecp_sym[j]:
                  strbuff += "\n%s" % (self._ecp_list[j])
            strbuff += "\n"

        strbuff += "  end\n"
        strbuff += "  Charge %s\n" % (self.charge)
        strbuff += "end\n"

        #User-defined options
        if self.optstr:
            strbuff += "%s" % (self.optstr)

        return strbuff


    @property
    def runargs(self):
        '''Override the default runargs'''

        # YL 09/11/2021: because ORCA uses OpenMPI and it's very likely ChemShell is driven by Intel MPI
        #                we need --oversubscribe to prevent the error
        #                "There are not enough slots available in the system to satisfy..."
        #                and --mca btl_base_warn_component_unused 0 to suppress the warning
        #                "unable to find any relevant network interfaces"
        if self.nprocs > 1:
            if self.CPU :
                return f'{self.input} "--oversubscribe -rf CPU --mca btl_base_warn_component_unused 0"'
            else:
                return f'{self.input} "--oversubscribe --mca btl_base_warn_component_unused 0"'
        else:
            return self.input


    def setOutKeys(self):
        '''Define {task:keyword} for searching in output file'''

        if self.frag.bqs:
            self.frag.nbqs = len(self.frag.bqs.coords)
            ncent = self.frag.natoms + self.frag.nbqs

        # each keyword should contain an array of integers specifying:
        #     [ row_0, # starting row
        #       row_n, # ending row
        #       row_i, # row increment
        #       col_0, # starting col
        #       col_n, # ending col
        #       col_i, # col increment
        #       skip , # skip the previous (skip-1) match,
        #       coeff, # unit conversion coefficient
        #     ]
        # referencing to the line where the key is matched
        self._outkeys = {
                          "energy"   : {'FINAL SINGLE POINT ENERGY':[0,0,1,5,5,1,3,1.0]},
                          "gradients": {"current gradient":[2,(1+3*(self.frag.natoms+self.num_explicit)),1,0,0,1,1,1.0]},
                          "bq_grads" : {"":[1,(self.frag.bqs.nbqs-self.num_explicit),1,0,2,1,1,1.0]},
                        }


    def parseMainOutput(self):
        '''Parse main output file self.output '''

        from ...utils import fileutils
        
        self.setOutKeys()

        self._result.energy    = fileutils.getArrayFromFile(self.output, 'out', self._result.energy.shape   , regex=self._outkeys['energy'])
        # If Explicit interface, need to remove BQ-BQ interaction
        if self.explicit:
          self._result.energy += self.energy_correction 

        if self._gradients and os.path.isfile(os.path.abspath(self.output_eandg)):
            temp_grad = zeros(shape=(self.frag.natoms+self.num_explicit,3))
            temp_grad = fileutils.getArrayFromFile(self.output_eandg, 'out', (self.frag.natoms+self.num_explicit, 3), regex=self._outkeys['gradients'])
            for i in range (self.frag.natoms+self.num_explicit):
              if (i >= self.num_explicit):
                self._result.gradients[i-self.num_explicit] = temp_grad[i] 

        if self._gradients and self.frag.nbqs:
            if os.path.isfile(os.path.abspath(self.output_bqs)):
               if self.explicit:
#              If this involves explicit interface, then the bq-bq forces need to be removed
                 self.frag.bqs.gradients = 0.0
                 temp_grads = zeros(shape=(self.frag.bqs.nbqs-self.num_explicit,3))
                 temp_grads = fileutils.getArrayFromFile(self.output_bqs, 'out', (self.frag.bqs.nbqs-self.num_explicit,3), regex=self._outkeys['bq_grads'])
                 exp_counter = 0
                 counter = 0
                 for i in range(self.frag.bqs.nbqs):
                   if i in self.exp_list:
                     self.frag.bqs.gradients[i] = temp_grad[exp_counter]
                     exp_counter += 1
                   else:
                     self.frag.bqs.gradients[i] = temp_grads[counter]
                     counter += 1
                 for i in self.exp_list:
                   coords_i = list(self.frag.bqs.coords[i])
                   for j in range(self.frag.bqs.nbqs):
                     chargeprod = 0.0
                     dist = 0.0
                     coords_j = list(self.frag.bqs.coords[j])
                     chargeprod=-1.0 * self.frag.bqs.charges[i] * self.frag.bqs.charges[j]
                     for k in range(3):
                       dist += (coords_i[k] - coords_j[k])**2
                     dist = math.sqrt(dist) 
                     if (j != i):
                       correction = chargeprod / (dist**3)
                       if (j in self.exp_list) and (j > i):
                         for k in range(3):
                           diff = coords_j[k] - coords_i[k]
                           self.frag.bqs.gradients[i][k] += correction  * diff
                           self.frag.bqs.gradients[j][k] -= correction  * diff
                       if j not in self.exp_list:
                         for k in range(3):
                           diff = coords_j[k] - coords_i[k]
                           self.frag.bqs.gradients[i][k] += correction * diff
                           self.frag.bqs.gradients[j][k] -= correction * diff

               else:
                 self.frag.bqs.gradients = fileutils.getArrayFromFile(self.output_bqs, 'out', self.frag.bqs.gradients.shape, regex=self._outkeys['bq_grads'])



