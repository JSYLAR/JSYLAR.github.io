提取帧为pdb
```
parm COM_box.prmtop 
trajin COM_box_md.nc 1000 1000
trajout 1000.pdb
run
```
RMSD&RMSF
``` 
parm COM_box.prmtop
trajin COM_box_md.nc
autoimage :1-500
strip :WAT
rms first
rms ToFirst :1-500&!@H= first out COM_rmsd.agr mass
rmsf byres out COM_rmsf.agr :1-500
run
``` 
距离
``` 
parm COM_box.prmtop 
trajin COMM_box_tmd3.nc 
distance distance1 :HEM@O1 :TAX@C18 out distance.agr
run
``` 
法向量二面角
``` 
parm COM_box.prmtop
trajin COM_box_md.nc
vector v_lig1 :500@C1,:500@C15,:500@C11 corrplane
vector v_lig2 :501@NA,:501@NB,:501@NC,:501@ND corrplane
vectormath vec1 v_lig1 vec2 v_lig2 dotangle out dotproduct.dat name acos(|V1|*|V2|)
``` 
聚类
``` 
parm COM_box.prmtop
trajin COM_box_tmd3.nc
cluster C0 \
    kmeans clusters 5 \
    rms :500 \
    sieve 10 random \
    out cnumvtime.dat \
    sil Sil \
    summary summary.dat \
    info info.dat \
    cpopvtime cpopvtime.agr normframe \
    repout rep repfmt restart \
    singlerepout singlerep.nc singlerepfmt netcdf
run
``` 
