# 一、依赖安装
### tcl安装
此处以tcl8.5.11为例
```
wget ftp://ftp.dl.ac.uk/qcg/ChemShell/tcl8.5.11-src.tar.gz
tar xvf tcl8.5.11-src.tar
cd tcl8.5.11/unix
./configure --prefix=/path/tcl8.5.11
make
make install
```
此外还以赖于gcc与openmpi或intelmpi
# 二、Tcl-chemshell安装
```
tar -xvzf chemsh-3.7.0.tar.gz
cd chemshell-3.7.0/src/config
```
安装串行版本
```
export CC=cc
export F77=gfortran
export F90=gfortran
export TCLROOT=/path/tcl8.5.11
export LIBTCL=/path/tcl8.5.11/lib/libtcl8.5.so
./configure
```
之后
```
cd ..
make
```
可能出现关于`mainf.f`中`arg`报错
打开位于`chemshell/src/chemsh`文件夹下的`mainf.f`将两行交换顺序
```
character(maxlen) :: arg
integer :: maxlen
```
改为
```
integer :: maxlen
character(maxlen) :: arg
```
并行版

```
export CC=mpicc
export F77=mpifort
export F90=mpifort
export COMPILER_IS_GFORTRAN=1
export TCLROOT=/path/tcl8.5.11
export LIBTCL=/path/tcl8.5.11/lib/libtcl8.5.so
./configure --with-mpi
cd ..
make
```

