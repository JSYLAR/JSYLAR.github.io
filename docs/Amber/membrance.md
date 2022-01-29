#  一、体系构建  
Amber含有识别膜的lipid14、17力场，但本身不支持生成膜，需要用第三方的手段，这里介绍使用CHARMM-GUI构建  
##  1、蛋白文件准备  
蛋白质文件是否含有配体无所谓，但必须包含链的信息，氨基酸命名等正常即可  
##  2、构建膜体系  
### 【1】进入CHARMM-GUI  
`https://charmm-gui.org/`  
需要注册登陆  
### 【2】进入膜构建页面  
右上方选择`input generator`后进入功能选项，选择`Membrane Builder`-`Bilayer Builder`  
### 【3】上传文件并勾选文件类型  
  
### 【4】根据需求建立膜  
下载`step5_assembly.pdb`重命名为`X.pdb`  
## 3、体系处理  
### 1、分子重命名  
  建立的体系中膜分子的命名Amber无法识别，需要使用Amber自带脚本进行转化  
  
```bash  
charmmlipid2amber.py -i X.pdb -o X_.pdb  
```  
支持转化的分子类型自行查询  
###  2、体系蛋白处理  
建立膜体系后的蛋白会存在Amber无法识别的`HSD`等问题，将其重新命名，并使用`pdb4amber`处理蛋白部分，膜部分使用`pdb4amber`会将一个磷脂拆分成三个分子，建议写个小脚本删除  
###  3、生成模拟体系  
  
```  
source leaprc.protein.ff19SB   
source leaprc.water.tip3p  
source leaprc.gaff  
source leaprc.lipid17  
loadamberparams Y.frcmod  
loadOff Y.lib  
complex = loadpdb X.pdb  
check complex  
set complex box { 100 100 140 }  
saveamberparm complex X_box.prmtop X_box.inpcrd  
savepdb complex X_ligs.pdb  
savepdb complex _box.pdb  
quit  
```  
其中周期盒子大小在建立膜时会给出，适当调整大小既可  

