``` 
parm COM_box.prmtop
trajin COM_box_md.nc
vector v_lig :TAX@C1,:TAX@C15,:TAX@C11 corrplane
vector v_hem :HEM@NA,:HEM@NB,:HEM@NC,:HEM@ND corrplane
vectormath vec1 v_lig vec2 v_hem dotangle out dotproduct.dat name acos(|V1|*|V2|)
``` 
