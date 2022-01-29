

#  限制性/共价对接
`LIG.cst`描述对接中共价连接或受限的两个原子间的各项参数  
```
#block 1 for covalent bond for CYM and CPD1

CST::BEGIN  
  TEMPLATE::   ATOM_MAP: 1 atom_name: FE1 N2 N1
  TEMPLATE::   ATOM_MAP: 1 residue3: HEM

  TEMPLATE::   ATOM_MAP: 2 atom_name: SG CB CA
  TEMPLATE::   ATOM_MAP: 2 residue3: CYM 
 
  CONSTRAINT:: distanceAB:    2.00   0.20 180.00  1
  CONSTRAINT::    angle_A:   98.00   3.00 100.00  360.00
  CONSTRAINT::    angle_B:  120.00  10.00  50.00  360.00
  CONSTRAINT::  torsion_A:  -98.00   5.00  50.00  360.00
  CONSTRAINT::  torsion_B:  103.00   5.00  25.00  360.00
  CONSTRAINT:: torsion_AB: -176.60   5.00   5.00  360.00
CST::END
```
OPTIONS

```
-in:file:s X.pdb
-in:file:extra_res_fa  Y.params
-in:file:extra_res_fa  Z.params
-run::preserve_header
-packing
	-ex1
	-ex2aro
	-ex2 
	-no_optH false
	-flip_HNQ true
	-ignore_ligand_chi true
-enzdes
	-cstfile LIG.cst
-parser
	-protocol ligand_dock_2018.xml

-out
-level 100
	-nstruct 10000
	-path:all outputs
	#-overwrite
```
在PDB首行通过REMARK声明两者连接  
```
REMARK   0 BONE TEMPLATE X HEM  1 MATCH MOTIF A CYM   443  1        
```
XML
```
<ROSETTASCRIPTS>
	<SCOREFXNS>
		<ScoreFunction name="ligand_soft_rep" weights="ligand_soft_rep">
		</ScoreFunction>
		<ScoreFunction name="hard_rep" weights="ligand">
		</ScoreFunction>
	</SCOREFXNS>

	<LIGAND_AREAS>
		<LigandArea name="docking_sidechain_X" chain="X" cutoff="6.0" add_nbr_radius="true" all_atom_mode="true" minimize_ligand="10"/>
		<LigandArea name="final_sidechain_X" chain="X" cutoff="6.0" add_nbr_radius="true" all_atom_mode="true"/>
		<LigandArea name="final_backbone_X" chain="X" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
		
		<LigandArea name="docking_sidechain_F" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="true" minimize_ligand="10"/>
		<LigandArea name="final_sidechain_F" chain="F" cutoff="6.0" add_nbr_radius="true" all_atom_mode="true"/>
		<LigandArea name="final_backbone_F" chain="F" cutoff="7.0" add_nbr_radius="false" all_atom_mode="true" Calpha_restraints="0.3"/>
	</LIGAND_AREAS>
	<INTERFACE_BUILDERS>
		<InterfaceBuilder name="side_chain_for_docking" ligand_areas="docking_sidechain_X,docking_sidechain_F"/>
		<InterfaceBuilder name="side_chain_for_final" ligand_areas="final_sidechain_X,final_sidechain_F"/>
		<InterfaceBuilder name="backbone" ligand_areas="final_backbone_X,final_backbone_F" extension_window="3"/>
	</INTERFACE_BUILDERS>
	<MOVEMAP_BUILDERS>
		<MoveMapBuilder name="docking" sc_interface="side_chain_for_docking" minimize_water="true"/>
		<MoveMapBuilder name="final" sc_interface="side_chain_for_final" bb_interface="backbone" minimize_water="true"/>
	</MOVEMAP_BUILDERS>
	<SCORINGGRIDS ligand_chain="X" width="20">
		<ClassicGrid grid_name="classic" weight="1.0"/>
	</SCORINGGRIDS>
	<MOVERS>
	single movers_X
		<AddOrRemoveMatchCsts name="cstadd" cst_instruction="add_new"/> add catalytic constraints
		<Transform name="transform_F" chain="F" box_size="7.0" move_distance="0.2" angle="20" cycles="700" repeats="1" temperature="5"/>
		<Transform name="transform_X" chain="X" box_size="8.0" move_distance="0.2" angle="20" cycles="700" repeats="1" temperature="5"/>
		<AddOrRemoveMatchCsts name="cstrem" cst_instruction="remove" keep_covalent="1"/> remove constraints
		<HighResDocker name="high_res_docker" cycles="6" repack_every_Nth="3" scorefxn="ligand_soft_rep" movemap_builder="docking"/>
		<FinalMinimizer name="final" scorefxn="hard_rep" movemap_builder="final"/>
		<AddOrRemoveMatchCsts name="cstfinadd" cst_instruction="add_pregenerated"/>
		<InterfaceScoreCalculator name="add_scores" chains="X,F" scorefxn="hard_rep"/>
		
	compound movers
		<ParsedProtocol name="low_res_dock">
			<Add mover_name="cstadd"/>
			<Add mover_name="transform_F"/>
			<Add mover_name="transform_X"/>
			<Add mover_name="cstrem"/>
		</ParsedProtocol>
		<ParsedProtocol name="high_res_dock">
			<Add mover_name="high_res_docker"/>
			<Add mover_name="final"/>
			<Add mover_name="cstfinadd"/>
		</ParsedProtocol>
	</MOVERS>
	<PROTOCOLS>
		<Add mover_name="low_res_dock"/>
		<Add mover_name="high_res_dock"/>
		<Add mover_name="add_scores"/>		
	</PROTOCOLS>
</ROSETTASCRIPTS>
```

