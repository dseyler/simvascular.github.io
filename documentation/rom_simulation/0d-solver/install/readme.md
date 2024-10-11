## Installation

There are three ways to install svZeroDSolver:

1. Download an installer from [SimTK Simvascular Downloads](https://simtk.org/frs/?group_id=188). 
2. Install using pip. This is the recommended method for using the Python API.
3. Build using CMake. This is the recommended method for using the C++ interface. 

Instructions on the pip and CMake installation methods are below.

### Using pip

For a pip installation, simply run the following command
(cloning of the repository is not required):

```bash
pip install git+https://github.com/simvascular/svZeroDSolver.git
```

### Using CMake

If you want to build svZeroDSolver manually from source, clone the repository
and run the following commands from the top directory of the project:

```bash
mkdir Release
cd Release
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```
<br/>
<details>
  <summary><mark><b>Note: Building on Sherlock for Stanford users</b></mark></summary>

```bash
module load cmake/3.23.1 gcc/14.2.0 binutils/2.38
mkdir Release
cd Release
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=/share/software/user/open/gcc/14.2.0/bin/g++ -DCMAKE_C_COMPILER=/share/software/user/open/gcc/14.2.0/bin/gcc ..
cmake --build .
```
</details>
<br/>
