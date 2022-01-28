# 一、环境
1.Ubuntu 20.04.1 LTS
2.gcc-8.4.0
3.cmake-3.16.3
4.系统带python3.8.5
5.GeForce RTX 3090*8
6.Driver Version: 455.32.00
7.CUDA Version: 11.1
8.其他依赖安装

```
apt -y update
apt -y install tcsh make
apt -y install  gcc gfortran 
apt -y install  flex bison patch 
apt -y install  bc xorg-dev libbz2-dev wget
```


AmberTools可以通过conda直接安装

```
conda install ambertools -c conda-forge
```

# 二、 Amber20安装[手册方法]
## 1.下载
Amber20.tar.bz2
AmberTools20.tar.bz2
## 2.解压

```
tar jxvf Amber20.tar.bz2
```
```
tar jxvf AmberTools20.tar.bz2
```
解压到文件夹`amber20_src`
## 3.进入文件夹

```
cd amber20_src
```

## 4.进入编译文件夹

```r
cd build
```
## 5.安装
`amber20`将安装于与`amber20_src`同一目录下，或在`run_cmake`修改
###  串行版本
```
./run_cmake
```
第一次执行后可能提示没有miniconda，再执行一次以上命令即会自动下载

```
make -j 20
```
```
make install
```
### 环境变量添加
```
soft=/home/name/soft
test -f /$soft/amber20/amber.sh  && source /$soft/amber20/amber.sh
```
### 并行版
下载`openmpi4.0.0`并解压到`amber20_src/AmberTools/src`

```
wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.bz2
```

```
tar jxvf openmpi-4.0.0.tar.bz2 -C path/to/amber20_src/AmberTools/src
```

```
cd path/to/amber20_src/AmberTools/src
```

```
/configure_openmpi gnu
```

修改`run_cmake`内

```
-DMPI=FALSE
```
为

```
-DMPI=TRUE
```
```
./run_cmake
```

```
make -j 20
```

```
make install
```
### GPU版本

修改`run_cmake`内

```
-DCUDA=FLASE
```
为

```
-DCUDA=TRUE
```
```
./run_cmake
```
```
make -j 20
```
```
make install
```
GPU版本会产生`pmemd.cuda`，混合精度浮点版本`pmemd.cuda_SPFP`与支持双精度浮点版本`pmemd.cuda_DPFP`
### GPU并行版本
修改`run_cmake`内

```
-DMPI=FALSE
-DCUDA=FLASE
```
为

```
-DMPI=TRUE
-DCUDA=TRUE
```
```
./run_cmake
```
```
make -j 20
```
```
make install
```
GPU并行版本会产生并行版本`pmemd.cuda_SPFP.MPI`与`pmemd.cuda_DPFP.MPI`,其中`pmemd.cuda_SPFP.MPI`即为之前版本的`pmemd.cuda.MPI`
###  NCCL多GPU通讯
安装对应cuda版本的nccl后添加

```
 -DNCCL=TRUE \
```

 到`run_cmake`43行之后再编译安装cuda并行版本即可
#  三、Amber20安装[官方网页方法]
http://ambermd.org/pmwiki/pmwiki.php/Main/CMake
在无root权限的服务器先安装了gcc-8.4.0与cmake3.20
```
cmake /path/amber20_src/ -DCMAKE_INSTALL_PREFIX=/path/amber20 -DCOMPILER=GNU -DMPI=TRUE  -DCUDA=TRUE
```
按手册的方法在显示成功但pdb4amber无法使用，使用该方法则没有问题
