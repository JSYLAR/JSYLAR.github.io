# 一、依赖安装
###  1.gcc-4.8.5安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy 

2.解压

```
tar -jxvf gcc-4.8.5.tar.bz2 
```

3.进入解压后的目录 

```
cd gcc-4.8.5 
```

4.下载和安装依赖库

```
./contrib/download_prerequisites 
```
7.编译安装

```
./configure --prefix=/path/gcc -enable-checking=release -enable-languages=c,c++,fortran -disable-multilib 
```

```
make 
```
```
make install
```
8.添加环境变量

###  2.anaconda3安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy

2.安装

```
bash ./Anaconda3-2020.11-Linux-x86_64.sh
```
###  3.openmpi-1.6.5安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy

2.解压

```
tar jxvf openmpi-1.6.5.tar.bz2
```
3.进入目录

```
cd openmpi-1.6.5
```
4.编译和安装
```
./configure --prefix=/path/openmpi
```
5.环境变量

```
#openmpi
export PATH=/path/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/path/openmpi/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/openmpi/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/path/openmpi/bin:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/openmpi/bin:$LIBRARY_PATH
```

###  4.zlib-1.2.11安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy

2.解压

```
tar zxvf zlib-1.2.11.tar.gz
```
3.进入目录

```
cd zlib-1.2.11
```
4.编译和安装
```
./configure --prefix=/path/zlib
```
```
make
```

```
make check
```

```
make install
```
5.环境变量
```
#zlib
export PATH=/path/zlib/lib:$PATH
export LD_LIBRARY_PATH=/path/zlib/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/zlib/lib:$LIBRARY_PATH
export PATH=/path/zlib/include:$PATH
export LD_LIBRARY_PATH=/path/zlib/include:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/zlib/include:$LIBRARY_PATH
```
###  5.szip-2.1.1安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy

2.解压

```
 tar zxvf szip-2.1.1.tar.gz
```
3.进入目录

```
cd szip-2.1.1
```
4.编译安装
```
./configure --prefix=/path/szip
```
```
make
```
```
make check
```
```
make install
```
5.环境变量
```
#szip
export PATH=/path/szip/lib:$PATH
export LD_LIBRARY_PATH=/path/szip/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/szip/lib:$LIBRARY_PATH
export PATH=/path/szip/include:$PATH
export LD_LIBRARY_PATH=/path/szip/include:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/szip/include:$LIBRARY_PATH
```
### 6.hdf5-1.12.0安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy

2.解压

```
 tar zxvf hdf5-1.12.0.tar.gz
```
3.进入目录

```
cd hdf5-1.12.0
```
4.编译安装

```
./configure --with-zlib=/path/zlib  --with-szlib=/path/szip --prefix=/path/hdf5 --enable-fortran --enable-parallel  --host=x86_64
```
```
make
```
```
make check
```
```
make install
```
5.环境变量
```
#hdf5
export PATH=/path/hdf5/bin:$PATH
export LD_LIBRARY_PATH=/path/hdf5/bin:$LD_LIBRARY_PATH
export PATH=/path/hdf5/lib:$PATH
export LD_LIBRARY_PATH=/path/hdf5/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/hdf5/lib:$LIBRARY_PATH
export PATH=/path/hdf5/include:$PATH
export LD_LIBRARY_PATH=/path/hdf5/include:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/hdf5/include:$LIBRARY_PATH
```
### 7.pnetcdf-1.12.1安装
1.下载
链接：https://pan.baidu.com/s/12yOB-nB3v86KsKjXDz2V9Q 
提取码：x6gy

2.解压

```
 tar zxvf pnetcdf-1.12.1.tar.gz
```
3.进入目录

```
cd pnetcdf-1.12.1
```
4.编译安装

```
 ./configure --prefix=/path/pnetcdf --with-mpi=/path/openmpi --enable-subfiling --enable-shared --enable-large-file-test --enable-null-byte-header-padding --enable-burst-buffering --enable-profiling --host=x86_64
```
```
make
```

```
make check
```

```
make install
```
5.环境变量

```
#pnetcdf
export PATH=/path/pnetcdf/lib:$PATH
export LD_LIBRARY_PATH=/path/pnetcdf/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/pnetcdf/lib:$LIBRARY_PATH
export PATH=/path/pnetcdf/include:$PATH
export LD_LIBRARY_PATH=/path/pnetcdf/include:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/pnetcdf/include:$LIBRARY_PATH
```
# 二、Amber安装
1.下载

2.解压

```
 tar xvf Amber18.tar
 tar xvf AmberTools19.tar
```
3.进入目录

```
cd amber18
```
4.添加环境变量

```
#Amber
test -f /path/amber18.sh  && source /path/amber18.sh
```
5.编译安装
###  串行版本
```
./configure --with-python /path/python gnu
```
```
make install
```
###  并行版本
```
./configure --with-python /path/bin/python --with-pnetcdf /path/pnetcdf/ -mpi gnu
```
```
make install
```
```
./configure --with-python /path/bin/python --with-pnetcdf /path/pnetcdf/ -openmp gnu
```
```
make openmp
```
###  GPU串行版本
```
./configure --with-python /path/bin/python -cuda gnu
```
```
make install
```
###  GPU并行版本
```
./configure --with-python /path/bin/python --with-pnetcdf /path/pnetcdf/ -cuda -mpi gnu
```
```
make install
```
###  环境变量
```
#Amber
export AMBERHOME=$soft/amber18
export PATH=$AMBERHOME/bin:$PATH
export PATH=$AMBERHOME/bat:$PATH
export LD_LIBRARY_PATH=$AMBERHOME/lib:$LD_LIBRARY_PATH
export MPI_HOME=$AMBERHOME/AmberTools
export LD_LIBRARY_PATH=$MPI_HOME/lib:$LD_LIBRARY_PATH
export DO_PARALLEL="mpirun -np 4"
export PYTHONPATH="${AMBERHOME}/lib/python3.8/site-packages:${PYTHONPATH}"
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH="/usr/local/cuda/lib:${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

