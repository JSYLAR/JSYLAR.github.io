### 1.下载

```csharp
https://mirrors.tuna.tsinghua.edu.cn/gnu/gcc/gcc-8.4.0/
```

###  2.解压

```csharp
tar zxvf gcc-8.4.0.tar.gz
cd gcc-8.4.0
```

###  3.下载依赖

```csharp
./contrib/download_prerequisites
```

###  4.创建编译文件夹

```csharp
mkdir bulidgcc
cd buildgcc
```
###  5.编译安装

```csharp
../configure -enable-checking=release -enable-languages=c,c++,fortran -disable-multilib --prefix=/path/gcc
make
make install
```

###  6.环境变量

```csharp
#gcc
export gcchome=/path/gcc
export PATH=$gcchome/bin:$PATH
export PATH=$gcchome/lib:$PATH
export PATH=$gcchome/lib64:$PATH
export LD_LIBRARY_PATH=$gcchome/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$gcchome/lib64:$LD_LIBRARY_PATH
export LIBRARY_PATH=$gcchome/lib:$LIBRARY_PATH
export LIBRARY_PATH=$gcchome/lib64:$LIBRARY_PATH
export PATH=$gcchome/include:$PATH
export LD_LIBRARY_PATH=$gcchome/include:$LD_LIBRARY_PATH
export LIBRARY_PATH=$gcchome/include:$LIBRARY_PATH
```

