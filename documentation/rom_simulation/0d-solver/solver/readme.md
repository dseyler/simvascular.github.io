# 0D Solver

Zero-dimensional (0D) models are lightweight methods to simulate bulk hemodynamic quantities in the cardiovascular system. Unlike 3D and 1D models, 0D models are purely time-dependent; they are unable to simulate spatial patterns in the hemodynamics. 0D models primarily simulate bulk cardiovascular flow rates and pressures; however, they can simulate other hemodynamic quantities, such as wall shear stress or volume, as well. Furthermore, 0D models are highly modular and compartmentalized, meaning different regions of the 0D models represent the hemodynamics in different parts of the cardiovascular anatomy being modeled.

0D models are analogous to electrical circuits. The flow rate simulated by 0D models represents electrical current, while the pressure represents voltage. Three primary building blocks of 0D models are resistors, capacitors, and inductors. Resistance captures the viscous effects of blood flow, capacitance represents the compliance and distensibility of the vessel wall, and inductance represents the inertia of the blood flow. Different combinations of these building blocks, as well as others, can be formed to reflect the hemodynamics and physiology of different cardiovascular anatomies.

svZeroDSolver is an application for performing 0D simulations of cardiovascular flows. Some noteworthy features of svZeroDSolver are:
* It is completely modular. Users can create custom flow models by arranging blocks corresponding to blood vessels, junctions, different types of boundary conditions, etc.
* It is written in C++ to enable high-performance applications.
* svZeroDSolver offers both a Python API and a C++ shared library to interface with other Python or C++-based applications. This allows it to be used in a fully coupled manner with other multi-physics solvers, and for parameter estimation, uncertainty quantification, etc.
* The svZeroDCalibrator application, which is included in svZeroDSolver, optimizes 0D blood vessel parameters to recapitulate given time-varying flow and pressure measurements (for example, from a high-fidelity 3D simulation). This allows users to build accurate 0D models that reflect observed hemodynamics.
* The svZeroDVisualization application enables users to visualize their 0D network and
interactively select nodes to view simulation results.
* The svZeroDGUI application allows users to generate input files for svZeroDSolver by
drawing the network on an easy-to-use GUI. This provides an alternative to manually
creating files and is useful for users without access to a 3D model.

The main categories of blocks implemented in svZeroDSolver are:
- Blood vessels
- Junctions
- Boundary conditions
- Heart chambers
- Heart valves

#### Installation

svZeroDSolver can be installed in two different ways. For using the Python
API, an installation via pip is recommended.

##### Using pip

For a pip installation, simply run the following command
(cloning of the repository is not required):

```bash
pip install git+https://github.com/simvascular/svZeroDSolver.git
```

##### Using CMake

If you want to build svZeroDSolver manually from source, clone the repository
and run the following commands from the top directory of the project:

```bash
mkdir Release
cd Release
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```


@remark <details>
  <summary>**Building on Sherlock**</summary>

```bash
module load cmake/3.23.1 gcc/12.1.0 binutils/2.38
mkdir Release
cd Release
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=/share/software/user/open/gcc/12.1.0/bin/g++ -DCMAKE_C_COMPILER=/share/software/user/open/gcc/12.1.0/bin/gcc ..
cmake --build .
```

</details>

#### 0D Solver Theory
We highlight here the theory behind the 0D solver. For equations and implementation details, we refer to the [documentation](https://simvascular.github.io/svZeroDSolver/index.html) throught this guide.

#### Governing equations
Flow rate, pressure, and other hemodynamic quantities in 0D models of vascular anatomies are governed by a system of nonlinear differential-algebraic equations, which are explained in more detail [here](https://simvascular.github.io/svZeroDSolver/class_sparse_system.html#details).

#### Time integration
We solve the differential-algebraic system implicitly in time, using the generalized-$\alpha$ method. The details to this method can be found [here](https://simvascular.github.io/svZeroDSolver/class_integrator.html#details).

#### Assembly
Similar to a finite element solver, the 0D solver defines local element contributions to the (sparse) [global system](https://simvascular.github.io/svZeroDSolver/class_sparse_system.html#details). The solver automatically assembles the local contributions into the global arrays. The local elements are referred to as blocks.

#### Blocks
An overview of all currently implemented blocks can be found [here](https://simvascular.github.io/svZeroDSolver/class_block.html). This collection of building blocks allows to model extensive and complex vascular networks. Many examples of vascular networks can be found [here](https://github.com/simvascular/svZeroDSolver/tree/master/tests/cases).
<!-- Todo: write and add link to Doxygen guide on adding new blocks here-->

#### References
Relevant literature can be found [here](https://simvascular.github.io/svZeroDSolver/citelist.html).
