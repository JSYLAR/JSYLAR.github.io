# 一、依赖安装
###  1.gcc安装
见`非root安装gcc-8.4.0`
###  2.lapack安装
```
wget http://www.netlib.org/lapack/lapack.tgz
```

在INSTALL文件夹中复制对应编译器的make.inc，此处使用gfortran

```
cp make.inc.gfortran ../make.inc
```
修改`make.inc`中内容，添加`-fPIC`参数，否则报错：

```
报错：... ... liblapack.a(dgelq2.o): relocation R_X86_64_32 against `.rodata' can not be used when making a shared object; recompile with -fPIC
```

```
CFLAGS = -O3 -fPIC
```
```
FC = gfortran
FFLAGS = -O2 -frecursive -fPIC
FFLAGS_DRV = $(FFLAGS)
FFLAGS_NOOPT = -O0 -frecursive -fPIC
```
修改`Makefile`文件中以下内容
```
.PHONY: lib
lib: lapacklib tmglib
#lib: blaslib variants lapacklib tmglib
```
安装

```
make
```
将当前路径添加至环境变量

```
export LIBRARY_PATH=/path/lapack-3.10.0/:$LIBRARY_PATH
```
#  二、pychenshell安装
注册并下载pychenshell包，`chemsh-py-21.0.0.tar.gz`

解压

```
tar xvf chemsh-py-21.0.0.tar.gz
cd chemsh-py-21.0.0
./setup --fc gfortran --cc gcc --pythonlib=/path/anaconda3/lib/libpython3.9.so --pythoninclude=/path/anaconda3/include/python3.9
```
并行版
```
./setup  --mpi --fc mpifort --cc mpicc --pythonlib=/path/anaconda3/lib/libpython3.9.so --mpi_include_path=/path/openmpi-4.1.1/include --mpi_lib_path=/path/openmpi-4.1.1/lib --pythoninclude=/path/anaconda3/include/python3.9
```
其他版本依照`INSTALL`文件内容安装，不再赘述
