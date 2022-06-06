在使用Rosetta做docking或其他应用时会碰到需要使用非标准氨基酸，有两种解决方法：  
一、将对应的氨基酸删除，添加一个修改后的氨基酸作为一个ligand添加到体系中，再将该ligand与主链连接到一起。  
二、定义一个新的氨基酸。  
这里记录第二种方法，以半胱氨酸为例，目的为去掉半胱氨酸连接在S上的氢，方便后续使用  
首先，进入Rosetta的氨基酸参数库，位于`path/rosetta/main/database/chemical/residue_type_sets`  
该文件夹下包含多个氨基酸库，一般只使用`fa_standard`中的参数  
进入`fa_standard`文件夹,其下的`residue_types.txt`为氨基酸参数的路径列表，`residue_types`文件夹下即为氨基酸参数  
#### 一、修改路径文件
修改`residue_types.txt`，在其中添加一行说明新氨基酸参数路径  
在`exclude_pdb_component_list.txt`中20种氨基酸外添加CYM残基  
```
residue_types/l-caa/CYX.params
```
#### 二、添加氨基酸参数
之后进入`residue_types`文件夹下的`l-caa`文件夹,其中包含了默认的氨基酸参数  
直接复制原本的`CYS.params`进行修改，重命名氨基酸，并删除有关S上的氢相关行即可  

```
NAME CYX
IO_STRING CYX X
TYPE POLYMER
AA UNK
ATOM  N   Nbb  NH1  -0.6046255 -0.350
ATOM  CA  CAbb CT1   0.0900506  0.100
ATOM  C   CObb C     0.6884871  0.550
ATOM  O   OCbb O    -0.6884871 -0.550
ATOM  CB  CH2  CT2  -0.1178426  0.000
ATOM  SG  SH1  S    -0.2463981 -0.290
ATOM  H   HNbb H     0.3987955  0.250
ATOM  HA  Hapo HB    0.1157793  0.000
ATOM 1HB  Hapo HA    0.0964167  0.000
ATOM 2HB  Hapo HA    0.0964167  0.000

LOWER_CONNECT N
UPPER_CONNECT C
BOND  N    CA 
BOND  N    H  
BOND  CA   C  
BOND  CA   CB 
BOND  CA   HA 
BOND_TYPE  C    O 2
BOND  CB   SG 
BOND  CB  1HB 
BOND  CB  2HB 
CHI 1  N    CA   CB   SG 
PROPERTIES PROTEIN ALPHA_AA L_AA SC_ORBITALS METALBINDING
METAL_BINDING_ATOMS O SG
DISULFIDE_ATOM_NAME SG
NBR_ATOM CB
NBR_RADIUS 3.4473
FIRST_SIDECHAIN_ATOM CB
RAMA_PREPRO_FILENAME all.ramaProb prepro.ramaProb
ACT_COORD_ATOMS SG END
ICOOR_INTERNAL    N      0.000000    0.000000    0.000000   N     CA    C  
ICOOR_INTERNAL    CA     0.000000  180.000000    1.458001   N     CA    C  
ICOOR_INTERNAL    C      0.000000   68.800003    1.523258   CA    N     C  
ICOOR_INTERNAL  UPPER  150.000000   63.800018    1.328685   C     CA    N  
ICOOR_INTERNAL    O    180.000000   59.200008    1.231015   C     CA  UPPER
ICOOR_INTERNAL    CB  -121.600000   69.400000    1.528861   CA    N     C  
ICOOR_INTERNAL    SG     0.000000   65.900000    1.808803   CB    CA    N  
ICOOR_INTERNAL   1HB   121.200000   70.500000    1.090249   CB    CA    SG 
ICOOR_INTERNAL   2HB   117.600000   70.500000    1.089821   CB    CA   1HB 
ICOOR_INTERNAL    HA  -119.000000   71.500000    1.090059   CA    N     CB 
ICOOR_INTERNAL  LOWER -150.000000   58.299995    1.328685   N     CA    C  
ICOOR_INTERNAL    H    180.000000   60.849998    1.010000   N     CA  LOWER
```
#### 三、修改其他相关文件
在使用该氨基酸对接时提示`prepro.ramaProb`中没有CYX的评分信息，位于`path/rosetta/main/database/scoring/score_functions/rama/fd`同样直接复制CYS的数据，重命名解决  

这样处理目前看起来一切正常，有什么不对的请指正
