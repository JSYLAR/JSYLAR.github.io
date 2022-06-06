
##    
使用rosetta对接时，需要将对接的小分子以及辅酶等非标准残基类分子进行处理，并重新命名各个原子，生成param文件以及重命名原子后的小分子pdb文件，再将小分子文件加回复合体pdb。
##  1.对接小分子处理
【1】小分子坐标调整  
用于对接的小分子通常不在蛋白质复合体`complex.pdb`文件中，需要首先调整小分子位置到合适的区域，因为一般会将小分子初始位置作为对接的起始位点，该步骤可以使用可视化的软件如`schrodinger`实现。  
【2】小分子构象搜索  
底物小分子，特别是略微复杂的小分子，通常有较多的可能构象，为了对接结果的准确，需要进行构象搜索，可以使用`obabel`或`schrodinger`，构象搜索将产生`X.sdf`文件，包含小分子的所有搜索到的构象，并以初始结构作为首个构象。  
【3】小分子param文件生成  
使用Rosetta的脚本`molfile_to_params.py`处理小分子构象库文件`X.sdf`  
```
  ython $rosetta/source/scripts/python/public/molfile_to_params.py -n X -p X --chain=F --clobber --conformers-in-one-file X.sdf
```
该步骤会产生`X_0001.pdb` `X.params` `X_conformers.pdb`,其中`X_conformers.pdb`为小分子构象库的pdb形式，`X_0001.pdb`是以conformers中第一个构象为结构，`X.params`为小分子参数文件。  
【4】小分子pdb添加到蛋白质文件内  
使用`notepad++`打开`X_0001.pdb`，将其复制到蛋白质pdb文件后  
##  2.其他小分子处理
除用于对接的小分子外，还可能有辅酶等不属于残基的分子在蛋白质中，这些分子同样需要处理，如无，跳过该步骤。  
【1】小分子导出  
使用`schrodinger`或其他软件将蛋白质复合体中的小分子导出为`mol2`格式，同时将其从蛋白删除  
【2】小分子parma文件生成  

```
  ython $rosetta/source/scripts/python/public/molfile_to_params.py -n XX XX.mol2 --chain=A --clobber
```
该步骤将产生`xx_0001.pdb` `xx.params`文件
【3】小分子pdb添加到蛋白质文件内
使用`notepad++`打开`xx_0001.pdb`，将其复制到蛋白质pdb文件后
##  *.仅包含两个及以下重原子分子处理
当小分子只包含两个及以下重原子时，会导致一个错误

```
ValueError: No acceptable neighbor atoms in molecule!
```
这种情况少见，涉及到`--m-ctrl`选项，需要创建一个文本文件，写入指定的作为`neighbor atoms`的原子信息，如下

```
M NBR 2
```
之后在`--m-ctrl`选项后指定该文件即可
##  3.xml文件
Rosetta的通过读取xml文件来设置参数，下面分别是单底物与多底物对接使用的protocol文件

### 单F链底物，以第一构象为初始位置进行对接xml
`dock_only_sub_F_tras.xml`
```
<ROSETTASCRIPTS>

		<SCOREFXNS>
			<ScoreFunction name="ligand_soft_rep" weights="ligand_soft_rep">
			</ScoreFunction>
			<ScoreFunction name="hard_rep" weights="ligand">
			</ScoreFunction>
		</SCOREFXNS>

		<LIGAND_AREAS>
			<LigandArea name="inhibitor_dock_sc" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_sc" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_bb" chain="F" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
		</LIGAND_AREAS>

		<INTERFACE_BUILDERS>
			<InterfaceBuilder name="side_chain_for_docking" ligand_areas="inhibitor_dock_sc"/>
			<InterfaceBuilder name="side_chain_for_final" ligand_areas="inhibitor_final_sc"/>
			<InterfaceBuilder name="backbone" ligand_areas="inhibitor_final_bb" extension_window="3"/>
		</INTERFACE_BUILDERS>

		<MOVEMAP_BUILDERS>
			<MoveMapBuilder name="docking" sc_interface="side_chain_for_docking" minimize_water="false"/>
			<MoveMapBuilder name="final" sc_interface="side_chain_for_final" bb_interface="backbone" minimize_water="false"/>
		</MOVEMAP_BUILDERS>

		<SCORINGGRIDS ligand_chain="F" width="15">
			<ClassicGrid grid_name="classic" weight="1.0"/>
		</SCORINGGRIDS>

		<MOVERS>
			<Transform name="transform" chain="F" box_size="6.0" move_distance="0.2" angle="20" cycles="500" repeats="1" temperature="5"/>
			<HighResDocker name="high_res_docker" cycles="6" repack_every_Nth="3" scorefxn="ligand_soft_rep" movemap_builder="docking"/>
			<FinalMinimizer name="final" scorefxn="hard_rep" movemap_builder="final"/>
			<InterfaceScoreCalculator name="add_scores" chains="F" scorefxn="hard_rep" native="complex.pdb"/> 
		</MOVERS>

		<PROTOCOLS>
			<Add mover_name="transform"/>
			<Add mover_name="high_res_docker"/>
			<Add mover_name="final"/>
			<Add mover_name="add_scores"/>
		</PROTOCOLS>


</ROSETTASCRIPTS>

```
### F链底物与X链底物以第一构象为初始位置对接xml

`dock_two_sub_tras.xml`
```
<ROSETTASCRIPTS>

		<SCOREFXNS>
			<ScoreFunction name="ligand_soft_rep" weights="ligand_soft_rep">
			</ScoreFunction>
			<ScoreFunction name="hard_rep" weights="ligand">
			</ScoreFunction>
		</SCOREFXNS>

		<LIGAND_AREAS>
			<LigandArea name="inhibitor_dock_sc_F" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_sc_F" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_bb_F" chain="F" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
			<LigandArea name="inhibitor_dock_sc_X" chain="X" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_sc_X" chain="X" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_bb_X" chain="X" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
		</LIGAND_AREAS>

		<INTERFACE_BUILDERS>
			<InterfaceBuilder name="side_chain_for_docking_F" ligand_areas="inhibitor_dock_sc_F"/>
			<InterfaceBuilder name="side_chain_for_final_F" ligand_areas="inhibitor_final_sc_F"/>
			<InterfaceBuilder name="backbone_F" ligand_areas="inhibitor_final_bb_F" extension_window="3"/>
			<InterfaceBuilder name="side_chain_for_docking_X" ligand_areas="inhibitor_dock_sc_X"/>
			<InterfaceBuilder name="side_chain_for_final_X" ligand_areas="inhibitor_final_sc_X"/>
			<InterfaceBuilder name="backbone_X" ligand_areas="inhibitor_final_bb_X" extension_window="3"/>
		</INTERFACE_BUILDERS>

		<MOVEMAP_BUILDERS>
			<MoveMapBuilder name="docking_F" sc_interface="side_chain_for_docking_F"/>
			<MoveMapBuilder name="final_F" sc_interface="side_chain_for_final_F" bb_interface="backbone_F"/>
			<MoveMapBuilder name="docking_X" sc_interface="side_chain_for_docking_X"/>
			<MoveMapBuilder name="final_X" sc_interface="side_chain_for_final_X" bb_interface="backbone_X"/>
		</MOVEMAP_BUILDERS>

		<SCORINGGRIDS ligand_chain="F" width="15">
			<ClassicGrid grid_name="classic" weight="1.0"/>
		</SCORINGGRIDS>

		<MOVERS>
			<Transform name="transform_F" chain="F" box_size="7.0" move_distance="0.2" angle="20" cycles="500" repeats="1" temperature="5"/>
			<Transform name="transform_X" chain="X" box_size="7.0" move_distance="0.2" angle="20" cycles="500" repeats="1" temperature="5"/>			
			<HighResDocker name="high_res_docker_F" cycles="6" repack_every_Nth="3" scorefxn="ligand_soft_rep" movemap_builder="docking_F"/>
			<HighResDocker name="high_res_docker_X" cycles="6" repack_every_Nth="3" scorefxn="ligand_soft_rep" movemap_builder="docking_X"/>
			<FinalMinimizer name="final_F" scorefxn="hard_rep" movemap_builder="final_F"/>
			<FinalMinimizer name="final_X" scorefxn="hard_rep" movemap_builder="final_X"/>
			<InterfaceScoreCalculator name="add_scores_F" chains="F" scorefxn="hard_rep" native="complex.pdb"/>
			<InterfaceScoreCalculator name="add_scores_X" chains="X" scorefxn="hard_rep" native="complex.pdb"/>			
		</MOVERS>

		<PROTOCOLS>
			<Add mover_name="transform_F"/>
			<Add mover_name="transform_X"/>
			<Add mover_name="high_res_docker_F"/>
			<Add mover_name="high_res_docker_X"/>
			<Add mover_name="final_F"/>
			<Add mover_name="final_X"/>
			<Add mover_name="add_scores_F"/>
			<Add mover_name="add_scores_X"/>
		</PROTOCOLS>


</ROSETTASCRIPTS>

```
### F链以指定坐标，X链以初始位置对接xml

`dock_two_sub_X_str_F_tras.xml`

```
<ROSETTASCRIPTS>

		<SCOREFXNS>
			<ScoreFunction name="ligand_soft_rep" weights="ligand_soft_rep">
			</ScoreFunction>
			<ScoreFunction name="hard_rep" weights="ligand">
			</ScoreFunction>
		</SCOREFXNS>

		<LIGAND_AREAS>
			<LigandArea name="inhibitor_dock_sc_F" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_sc_F" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_bb_F" chain="F" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
			<LigandArea name="inhibitor_dock_sc_X" chain="X" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_sc_X" chain="X" cutoff="6.0" add_nbr_radius="true" all_atom_mode="false"/>
			<LigandArea name="inhibitor_final_bb_X" chain="X" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
		</LIGAND_AREAS>

		<INTERFACE_BUILDERS>
			<InterfaceBuilder name="side_chain_for_docking_F" ligand_areas="inhibitor_dock_sc_F"/>
			<InterfaceBuilder name="side_chain_for_final_F" ligand_areas="inhibitor_final_sc_F"/>
			<InterfaceBuilder name="backbone_F" ligand_areas="inhibitor_final_bb_F" extension_window="3"/>
			<InterfaceBuilder name="side_chain_for_docking_X" ligand_areas="inhibitor_dock_sc_X"/>
			<InterfaceBuilder name="side_chain_for_final_X" ligand_areas="inhibitor_final_sc_X"/>
			<InterfaceBuilder name="backbone_X" ligand_areas="inhibitor_final_bb_X" extension_window="3"/>
		</INTERFACE_BUILDERS>

		<MOVEMAP_BUILDERS>
			<MoveMapBuilder name="docking_F" sc_interface="side_chain_for_docking_F"/>
			<MoveMapBuilder name="final_F" sc_interface="side_chain_for_final_F" bb_interface="backbone_F"/>
			<MoveMapBuilder name="docking_X" sc_interface="side_chain_for_docking_X"/>
			<MoveMapBuilder name="final_X" sc_interface="side_chain_for_final_X" bb_interface="backbone_X"/>
		</MOVEMAP_BUILDERS>

		<SCORINGGRIDS ligand_chain="F" width="15">
			<ClassicGrid grid_name="classic" weight="1.0"/>
		</SCORINGGRIDS>

		<MOVERS>
			<Transform name="transform" chain="F" box_size="7.0" move_distance="0.2" angle="20" cycles="500" repeats="1" temperature="5"/>
			<StartFrom name="startform" chain="X">
			<Coordinates x="31" y="4" z="-14"/>
		</StartFrom>
			<HighResDocker name="high_res_docker_F" cycles="6" repack_every_Nth="3" scorefxn="ligand_soft_rep" movemap_builder="docking_F"/>
			<HighResDocker name="high_res_docker_X" cycles="6" repack_every_Nth="3" scorefxn="ligand_soft_rep" movemap_builder="docking_X"/>
			<FinalMinimizer name="final_F" scorefxn="hard_rep" movemap_builder="final_F"/>
			<FinalMinimizer name="final_X" scorefxn="hard_rep" movemap_builder="final_X"/>
			<InterfaceScoreCalculator name="add_scores_F" chains="F" scorefxn="hard_rep" native="complex.pdb"/>
			<InterfaceScoreCalculator name="add_scores_X" chains="X" scorefxn="hard_rep" native="complex.pdb"/>			
		</MOVERS>

		<PROTOCOLS>
			<Add mover_name="transform"/>
			<Add mover_name="startform"/>
			<Add mover_name="high_res_docker_F"/>
			<Add mover_name="high_res_docker_X"/>
			<Add mover_name="final_F"/>
			<Add mover_name="final_X"/>
			<Add mover_name="add_scores_F"/>
			<Add mover_name="add_scores_X"/>
		</PROTOCOLS>


</ROSETTASCRIPTS>

```
## 4.输入文件options
options文件是rosetta执行对接的输入文件，在其中指定了要导入的`.params`文件、蛋白质复合体文件`complex.pdb`以及`protocol`文件，对接结果数等多个参数，以下为F与X两个底物对接10000个结果的`options`文件

```
#Pound signs indicate comments 

#-in:file:s option imports the protein and ligand PDB structures
#-in:file:extra_res_fa option imports the parameters for the ligand

-in
	-file
		-s complex.pdb
		-extra_res_fa F.params
		-extra_res_fa X.params

#the packing options allow Rosetta to sample additional rotamers for
#protein sidechain angles chi 1 (ex1) and chi 2 (ex2) 
#no_optH false tells Rosetta to optimize hydrogen placements
#flip_HNQ tells Rosetta to consider HIS,ASN,GLN hydrogen flips
#ignore_ligand_chi prevents Roseta from adding additional ligand rotamer

-packing
	-ex1
	-ex2
	-no_optH false
	-flip_HNQ true
	-ignore_ligand_chi true


#parser:protocol locates the XML file for RosettaScripts

-parser
	-protocol dock_two_sub_tras.xml

#overwrite allows Rosetta to write over previous structures and scores

-overwrite

#Ligand docking is not yet benchmarked with the updated scoring function
#This flag restores certain parameters to previously published values

-mistakes
	-restore_pre_talaris_2013_behavior true
-nstruct 10000 
```
##  5.docking

```
mpirun -np 64 $rosetta/source/bin/rosetta_scripts.mpi.linuxgccrelease @options 
```

##  6.结果处理
所有的对接结果的各项打分均在score.sc文件中，可根据打分来分析挑选结果。


