parm位于`amber20/dat/antechamber/PARMCHK.DAT`  
ff14sb位于amber20/dat/leap/cmd/  
做包含金属的QM/MM时如果在ff14sb中没有该原子，会有错误  
可以在source leaprc.protein.ff14SB同时source leaprc.ffPM3解决
