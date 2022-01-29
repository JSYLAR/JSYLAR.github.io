### 适用于Amber18\20版本  
使用Amber做带小分子配体的MD时，由于Amber无法识别小分子，需要对小分子做处理，相比于单纯蛋白分子的MD步骤会繁琐一些，在此记录一下。  
###  一、文件准备  
####  1.文件检查与拆分  
含配体的复合体pdb文件可以来自晶体或对接结果，其中小分子与蛋白分子的相对位置将会是MD的初始位置，在准备过程中需要检查确认。  
  
【1】首先在可视化软件如薛定谔等检查复合体中小分子，确保其键连准确，没有原子，特别是氢原子的缺失。  
  
【2】检查完毕后保存复合体文件，使用文本编辑器打开，推荐使用`notepad++`，找到对应小分子的行，将其剪切到新的文本中，命名为`Y.pdb`，剩余的蛋白分子命名为`X.pdb`  
####  2.小分子文件处理  
  
【3】使用Amber的工具antechamber将小分子pdb文件转为mol2文件  
  
```  
antechamber -i Y.pdb -fi pdb -o Y.mol2 -fo mol2 -c bcc -s 2  
```  
如果小分子配体较为复杂，此处会耗费较长的时间。  
`注意：此处使用bcc计算分子的电荷分布，其准确性低于RESP，如果懂得使用gaussian或Multiwfn，建议使用RESP计算的电荷`  
  
【4】得到`Y.mol2`文件后，使用parmchk2产生小分子参数文件  
  
```  
parmchk2 -i Y.mol2 -f mol2 -o Y.frcmod  
```  
【5】新建文件`Y.tleap`，写入以下内容  
  
```  
source leaprc.gaff  
Y = loadmol2 Y.mol2   
check Y  
loadamberparams Y.frcmod  
check Y  
saveoff Y Y.lib   
saveamberparm Y Y.prmtop Y.inpcrd  
quit  
```  
【6】使用`tleap`程序，生成小分子`Y.lib`文件  
  
```  
tleap -f Y.tleap  
```  
至此得到`Y.frcmod` `Y.lib` `Y.prmtop` `Y.inpcrd` 文件。  
  
**`这里碰到一个问题，在处理带有磷酸基团的小分子时，如果为磷酸基团添加氢原子，在MD过程中，磷酸基团的氢原子会快速无序摆动，导致整个模拟体系崩溃，在体系加热过程中的体现为温度大范围波动，并远远超出设置的上限，报错显示浮点超出上限或非法内存访问，去除磷酸基团的氢原子后一切恢复正常，报错信息如下。`**  
  
```  
Error: an illegal memory access was encountered launching kernel kNLSkinTest  
```  
  
####  3.蛋白质文件处理  
【7】使用文本编辑器打开`X.pdb`文件，删掉除原子信息外的所有行，只保留如下的行  
  
```  
...  
...  
ATOM  16100  N   LEU B 537      18.387 -77.040 -41.003  1.00  0.80           N    
ATOM  16101  CA  LEU B 537      19.579 -76.228 -41.346  1.00  0.80           C    
ATOM  16102  C   LEU B 537      20.327 -75.718 -40.033  1.00  0.80           C    
ATOM  16103  O   LEU B 537      20.000 -76.288 -38.963  1.00  0.80           O    
ATOM  16104  CB  LEU B 537      19.148 -74.980 -42.190  1.00  0.80           C    
ATOM  16105  CG  LEU B 537      18.636 -75.198 -43.626  1.00  0.80           C    
ATOM  16106  CD1 LEU B 537      18.176 -73.876 -44.243  1.00  0.80           C    
ATOM  16107  CD2 LEU B 537      19.672 -75.869 -44.530  1.00  0.80           C    
ATOM  16108  OXT LEU B 537      21.005 -74.658 -40.138  1.00  0.80           O1-  
ATOM  16109  H   LEU B 537      18.021 -76.812 -40.085  1.00  0.00           H    
ATOM  16110  HA  LEU B 537      20.334 -76.831 -41.849  1.00  0.00           H    
ATOM  16111  HB3 LEU B 537      20.001 -74.318 -42.301  1.00  0.00           H    
ATOM  16112  HB2 LEU B 537      18.389 -74.435 -41.628  1.00  0.00           H    
ATOM  16113  HG  LEU B 537      17.759 -75.840 -43.564  1.00  0.00           H    
ATOM  16114 HD11 LEU B 537      17.370 -74.053 -44.953  1.00  0.00           H    
ATOM  16115 HD12 LEU B 537      17.814 -73.195 -43.476  1.00  0.00           H    
ATOM  16116 HD13 LEU B 537      18.989 -73.377 -44.769  1.00  0.00           H    
ATOM  16117 HD21 LEU B 537      19.253 -76.103 -45.506  1.00  0.00           H    
ATOM  16118 HD22 LEU B 537      20.558 -75.250 -44.669  1.00  0.00           H    
ATOM  16119 HD23 LEU B 537      19.998 -76.804 -44.088  1.00  0.00           H    
TER   16120      LEU B 537  
```  
【8】使用Amber的工具`pdb for amber`删除模型内氢原子  
  
```  
pdb4amber -i X.pdb -o X_noH.pdb -y --dry  
```  
【9】以Amber的氢命名方式重新添加氢原子  
```  
reduce X_noH.pdb > X_H.pdb  
```  
【10】使用pdb4amber对加氢后的pdb文件进行处理  
```  
pdb4amber -i X_H.pdb -o X.pdb  
```  
至此得到Amber标准的蛋白质分子文件`X.pdb`  
####  4.复合体文件处理  
【11】将`Y.pdb`使用文本编辑器打开，将原子信息复制到`X.pdb`文件后，重命名为`com.pdb`  
  
【12】创建新文件`com.tleap`写入以下内容，保存  
```  
source leaprc.protein.ff14SB `此处可以使用ff19SB`   
source leaprc.water.tip3p  
source leaprc.gaff  
loadamberparams Y.frcmod  
loadoff Y.lib  
complex = loadpdb com.pdb  
check complex  
solvatebox complex TIP3PBOX 12.0  
addions2 complex Na+ 0  
addions2 complex Cl- 0  
saveamberparm complex X_box.prmtop X_box.inpcrd  
savepdb complex X_box.pdb  
quit  
```  
` 此处可以使用ff19SB`   
【13】使用`tleap`程序，生成复合体参数文件`X_box.prmtop` `X_box.inpcrd`文件以及水盒文件`X_box.pdb`  
```  
tleap -f com.tleap  
```  
至此，得到`X_box.prmtop`、`X_box.inpcrd`、`X_box.pdb`  
###  二、分子动力学模拟  
####  1.能量最小化  
【1】约束主链最小化`min1.in`  
```  
 &cntrl    
  imin=1,   
  maxcyc=10000,   
  ncyc=5000,   
  ntb=1,   
  ntr=1,  
  restraintmask=':1-1104',   
  restraint_wt=2,  
  cut=8.0   
 /   
 END  
```  
执行命令  
```  
pmemd.cuda -O -i min1.in -o X_box_min1.out -p X_box.prmtop -c X_box.inpcrd -r X_box_min1.rst -ref X_box.inpcrd  
```  
【2】无约束最小化`min2.in`  
```  
 &cntrl    
  imin=1,   
  maxcyc=100000,   
  ncyc=5000,   
  ntb=1,   
  ntc=1,  
  ntf=1,   
  ntpr=10,  
  cut=8.0   
 /   
 END  
```  
执行命令  
```  
pmemd.cuda -O -i min2.in -o X_box_min2.out -p X_box.prmtop -c X_box_min1.rst -r X_box_min2.rst  
```  
####  2.体系加热  
【3】约束主链恒容50ps加热`heat.in`  
```  
explicit solvent initial heating: 50ps  
 &cntrl  
  imin=0,  
  irest=0,  
  nstlim=25000, dt=0.002,  
  ntc=2, ntf=2, ntx=1,  
  cut=8.0, ntb=1,  
  ntpr=500, ntwx=500,  
  ntt=3, gamma_ln=2.0,  
  tempi=0.0, temp0=300.0, ig=-1,  
  ntr=1,  
  restraintmask=':1-1104',  
  restraint_wt=2.0,  
  iwrap=1  
  nmropt=1  
  /  
  &wt TYPE='TEMP0', ISTEP1=0, ISTEP2=25000,  
  VALUE1=0.0, VALUE2=300.0, /  
  &wt TYPE = 'END' /   
 END  
```  
执行命令  
```  
pmemd.cuda -O -i heat.in -o X_box_heat.out -p X_box.prmtop -c X_box_min2.rst -r X_box_heat.rst -x X_box_heat.nc -ref X_box_min2.rst  
```  
####  3.恒压平衡  
【4】50ps平衡`press.in`  
```  
explicit solvent density: 50ps  
 &cntrl  
  imin=0,  
  irest=1,  
  ntx=5,  
  nstlim=25000, dt=0.002,  
  ntc=2, ntf=2,  
  cut=8.0, ntb=2, ntp=1, taup=2.0,  
  ntpr=500, ntwx=500,  
  ntt=3, gamma_ln=2.0,  
  temp0=300.0, ig=-1,  
  ntr=0,  
  /   
 END  
```  
执行命令  
```  
pmemd.cuda -O -i press.in -o X_box_press.out -p X_box.prmtop -c X_box_heat.rst -r X_box_press.rst -x X_box_press.nc -ref X_box_heat.rst  
```  
####  4.全局平衡  
【5】10ns平衡`eq.in`  
```  
&cntrl  
  imin=0, irest=1, ntx=5,  
  nstlim=5000000, dt=0.002,  
  ntc=2, ntf=2,  
  cut=10.0, ntb=2, ntp=1, taup=2.0,  
  ntpr=500, ntwx=500, ntwr=5000,  
  ntt=3, gamma_ln=2.0,  
  temp0=300.0,  
 /   
 END  
```  
执行命令  
```  
pmemd.cuda -O -i eq.in -o X_box_eq.out -p X_box.prmtop -c X_box_press.rst -r X_box_eq.rst -x X_box_eq.nc  
```  
####  5.正式模拟  
【6】100ns模拟`md.in`  
```  
explicit solvent production run: 100ns  
 &cntrl  
  imin=0,  
  irest=1,  
  ntx=5,  
  nstlim=50000000, dt=0.002,  
  ntc=2, ntf=2,  
  cut=8.0, ntb=2, ntp=1, taup=2.0,  
  ntpr=5000, ntwx=5000, ntwr=50000,  
  ntt=3, gamma_ln=2.0,  
  temp0=300.0, ig=-1,  
  iwrap=1  
  /   
 END  
```  
执行命令  
```  
pmemd.cuda -O -i md.in -o X_box_md.out -p X_box.prmtop -c X_box_eq.rst -r X_box_md.rst -x X_box_md.nc  
```  
  

