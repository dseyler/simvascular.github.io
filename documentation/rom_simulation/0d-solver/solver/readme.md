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
<ul>
  <li>Blood vessels</li>
  <li>Junctions</li>
  <li>Boundary conditions</li>
  <li>Heart chambers</li>
  <li>Heart valves</li>
</ul>

## Installation

svZeroDSolver can be installed in two different ways. For using the Python API, an installation via pip is recommended.

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

## Blocks

The modular architecture of svZeroDSolver relies on "blocks", such as blood vessels, junctions, valves, boundary conditions, etc. Users can assemble and connect these blocks together in a variety of ways to create extensive and customizable 0D circulation models.   

An overview of all currently implemented blocks can be found [here](https://simvascular.github.io/svZeroDSolver/class_block.html). This collection of building blocks allows to model extensive and complex vascular networks. Many examples of vascular networks can be found [here](https://github.com/simvascular/svZeroDSolver/tree/master/tests/cases). The assembly of these blocks is specified in the `.json` configuration file. The user guide below provides details.

We are always interested in adding new blocks to expand the funcitonality of svZeroDSolver. For developers interested in contributing, please read the [Developer Guide](https://simvascular.github.io/svZeroDSolver/developer_guide.html). 

## svZeroDSolver - Quick User Guide

svZeroDSolver can be used to run zero-dimensional (0D) cardiovascular
simulations based on a given configuration.

### Run svZeroDSolver from the command line

svZeroDSolver can be executed from the command line using a JSON configuration
file.

```bash
svzerodsolver tests/cases/steadyFlow_RLC_R.json result_steadyFlow_RLC_R.csv
```

The result will be written to a CSV file.

### Run svZeroDSolver from other programs

For some applications it is beneficial to run svZeroDSolver directly
from within another program. For example, this can be
useful when many simulations need to be performed (e.g. for
calibration, uncertainty quantification, ...). It is also allows using
svZeroDSolver with other solvers, for example as boundary conditions or
forcing terms.

#### In C++

SvZeroDSolver needs to be built using CMake to use the shared library interface.

Detailed examples of interfacing with svZeroDSolver from C++ codes are available
in the test cases at `svZeroDSolver/tests/test_interface`.

#### In Python

Please make sure that
you installed svZerodSolver via pip to enable this feature. We start by
importing pysvzerod:

```python
>>> import pysvzerod
```

Next, we create a solver from our configuration. The configuration can
be specified by either a path to a JSON file:

```python
>>> solver = pysvzerod.Solver("tests/cases/steadyFlow_RLC_R.json")
```

or as a Python dictionary:

```python
>>> my_config = {...}
>>> solver = pysvzerod.Solver(my_config)
```

To run the simulation we add:

```python
>>> solver.run()
```

The simulation result is now saved in the solver instance. We can obtain
results for individual degrees-of-freedom (DOFs) as
```python
>>> solver.get_single_result("flow:INFLOW:branch0_seg0")

array([5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.,
       5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.,
       5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.,
       5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.,
       5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.,
       5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.])
```
The naming of the DOFs is similar to how results are written if the simulation
option `output_variable_based` is activated (see below). We can also obtain
the mean result for a DOF over time with:
```python
>>> solver.get_single_result_avg("flow:INFLOW:branch0_seg0")

5.0
```

Or the result of the full simulation as a pandas data frame:

```python
>>> solver.get_full_result()

             name  time  flow_in  flow_out  pressure_in  pressure_out
0    branch0_seg0  0.00      5.0       5.0       1100.0         600.0
1    branch0_seg0  0.01      5.0       5.0       1100.0         600.0
2    branch0_seg0  0.02      5.0       5.0       1100.0         600.0
3    branch0_seg0  0.03      5.0       5.0       1100.0         600.0
4    branch0_seg0  0.04      5.0       5.0       1100.0         600.0
..            ...   ...      ...       ...          ...           ...
96   branch0_seg0  0.96      5.0       5.0       1100.0         600.0
97   branch0_seg0  0.97      5.0       5.0       1100.0         600.0
98   branch0_seg0  0.98      5.0       5.0       1100.0         600.0
99   branch0_seg0  0.99      5.0       5.0       1100.0         600.0
100  branch0_seg0  1.00      5.0       5.0       1100.0         600.0

[101 rows x 6 columns]
```

There is also a function to retrieve the full result directly based on a given configuration:

```python

>>> my_config = {...}
>>> pysvzerod.simulate(my_config)

             name  time  flow_in  flow_out  pressure_in  pressure_out
0    branch0_seg0  0.00      5.0       5.0       1100.0         600.0
1    branch0_seg0  0.01      5.0       5.0       1100.0         600.0
2    branch0_seg0  0.02      5.0       5.0       1100.0         600.0
3    branch0_seg0  0.03      5.0       5.0       1100.0         600.0
4    branch0_seg0  0.04      5.0       5.0       1100.0         600.0
..            ...   ...      ...       ...          ...           ...
96   branch0_seg0  0.96      5.0       5.0       1100.0         600.0
97   branch0_seg0  0.97      5.0       5.0       1100.0         600.0
98   branch0_seg0  0.98      5.0       5.0       1100.0         600.0
99   branch0_seg0  0.99      5.0       5.0       1100.0         600.0
100  branch0_seg0  1.00      5.0       5.0       1100.0         600.0

[101 rows x 6 columns]

```

### Configuration

svZeroDSolver is configured using either a JSON file or a Python
dictionary. The top-level structure of both is:

```python
{
    "simulation_parameters": {...},
    "vessels": [...],
    "junctions": [...],
    "boundary_conditions": [...]
}
```

In the following sections, the individual categories are described in more
detail.

#### Simulation parameters

The svZeroDSolver can be configured with the following options in the
`simulation_parameters` section of the input file. Parameters without a
default value must be specified.

|Parameter key                                  | Description                                                 | Default value |
|-----------------------------------------------|------------------------------------------------------------ | --------------|
|`number_of_cardiac_cycles` &emsp;              | Number of cardiac cycles to simulate &emsp;                        | - |
|`number_of_time_pts_per_cardiac_cycle` &emsp;  | Number of time steps per cardiac cycle &emsp;                      | - |
|`absolute_tolerance` &emsp;                    | Absolute tolerance for time integration &emsp;                    | $10^{-8}$ |
|`maximum_nonlinear_iterations` &emsp;          | Maximum number of nonlinear iterations for time integration &emsp; | $30$ |
|`steady_initial` &emsp;                        | Toggle whether to use the steady solution as the initial condition for the simulation &emsp; | true |
|`output_variable_based` &emsp;                 | Output solution based on variables (i.e. flow and pressure at nodes and internal variables) &emsp; | false |
|`output_interval` &emsp;                       | The frequency of writing timesteps to the output (1 means every timestep is written) &emsp; | $1$ |
|`output_mean_only` &emsp;                      | Write only the mean values over every timestep to output file &emsp; | false |
|`output_derivative` &emsp;                     | Write time derivatives to output file &emsp; | false |
|`output_all_cycles` &emsp;                     | Write all cardiac cycles to output file &emsp; | false |
|`use_cycle_to_cycle_error` &emsp;              | Use cycle-to-cycle error to determine number of cycles for convergence &emsp; | false |
|`sim_cycle_to_cycle_percent_error` &emsp;      | Percentage error threshold for cycle-to-cycle pressure and flow difference &emsp; | 1.0 |

The option `use_cycle_to_cycle_error` allows the solver to change the number of cardiac cycles it runs depending on the cycle-to-cycle convergence of the simulation. For simulations with no RCR boundary conditions, the simulation will add extra cardiac cycles until the difference between the mean pressure and flow in consecutive cycles is below the threshold set by `sim_cycle_to_cycle_percent_error` at all inlets and outlets of the model. If there is at least one RCR boundary condition, the number of cycles is determined based on equation 21 of Pfaller et al. (2021), using the RCR boundary condition with the largest time constant.


<style>
table{
    border-collapse: collapse;
    border-spacing: 100000px;
    border:1px solid #000000;
}

th{
    border:0.5px solid #000000;
    padding: 15px;
}

td{
    border:0.5px solid #000000;
    padding: 5px;
}
</style>

#### Vessels

More information about the vessels can be found in their respective class references. Below is a template vessel block with boundary conditions, `INFLOW` and `OUT`, at its inlet and outlet respectively.

```python
{
    "boundary_conditions": {
        "inlet": "INFLOW", # Optional: Name of inlet boundary condition
        "outlet": "OUT", # Optional: Name of outlet boundary condition
    },
    "vessel_id": 0, # ID of the vessel
    "vessel_name": "branch0_seg0", # Name of vessel
    "zero_d_element_type": "BloodVessel", # Type of vessel
    "zero_d_element_values": {...} # Values for configuration parameters
}
```

| Description                              | Class                       | `zero_d_element_type` &emsp; | `zero_d_element_values` &emsp; |
| ---------------------------------------- | --------------------------- | --------------------- | ------------------------|
| Blood vessel with optional stenosis &emsp;      | BloodVessel &emsp;                 | `BloodVessel` &emsp;         | `C`: Capacitance <br> `L`: Inductance <br> `R_poiseuille`: Poiseuille resistance <br> `stenosis_coefficient`: Stenosis coefficient &emsp; |


#### Junctions

More information about the junctions can be found in their respective class references. Below is a template junction block that connects vessel ID 0 with vessel IDs 1 and 2.

```python
{
    "junction_name": "J0", # Name of the junction
    "junction_type": "BloodVesselJunction", # Type of the junction
    "inlet_vessels": [0], # List of vessel IDs connected to the inlet
    "outlet_vessels": [1, 2], # List of vessel IDs connected to the inlet
    "junction_values": {...} # Values for configuration parameters
}
```

Description &emsp;                          | Class &emsp;               | `junction_type` &emsp;      | `junction_values` &emsp;
------------------------------------- | ---------------------| --------------------- | -----------
Purely mass conserving junction &emsp; | Junction &emsp;             | `NORMAL_JUNCTION` &emsp;     | - &emsp;
Resistive junction &emsp;                 | ResistiveJunction &emsp;    | `resistive_junction` &emsp;  | `R`: Ordered list of resistances for all inlets and outlets &emsp;
Blood vessel junction &emsp;             | BloodVesselJunction &emsp;  | `BloodVesselJunction` &emsp; | Same as for `BloodVessel` element but as ordered list for each inlet and outlet &emsp;

#### Boundary conditions

More information about the boundary conditions can be found in their respective class references. Below is a template `FLOW` boundary condition.

```python
{
    "bc_name": "INFLOW", # Name of the boundary condition
    "bc_type": "FLOW", # Type of the boundary condition
    "bc_values": {...} # Values for configuration parameters
},
```

Description &emsp;                           | Class &emsp;                  | `bc_type` &emsp;             | `bc_values` &emsp;
------------------------------------- | ---------------------- | --------------------- | -----------
Prescribed (transient) flow &emsp;           | FlowReferenceBC &emsp;        | `FLOW` &emsp;                | `Q`: Time-dependent flow values <br> `t`: Time steps <br> `fn`: Mathematical expression <br> Note: Either specify `Q` and `t` together, or just `fn` &emsp;
Prescribed (transient) pressure &emsp;       | PressureReferenceBC &emsp;    | `PRESSURE` &emsp;            | `P`: Time-dependent pressure values <br> `t`: Time steps <br> `fn`: Mathematical expression <br> Note: Either specify `Q` and `t` together, or just `fn` &emsp;
Resistance &emsp;                            | ResistanceBC &emsp;           | `RESISTANCE` &emsp;          | `R`: Resistance <br> `Pd`: Time-dependent distal pressure <br> `t`: Time stamps &emsp;
Windkessel or RCR &emsp;                            | WindkesselBC &emsp;           | `RCR` &emsp;                 | `Rp`: Proximal resistance <br> `C`: Capacitance <br> `Rd`: Distal resistance <br> `Pd`: Distal pressure &emsp;
Coronary outlet &emsp;                       | OpenLoopCoronaryBC &emsp;     | `CORONARY` &emsp;            | `Ra`: Proximal resistance <br> `Ram`: Microvascular resistance <br> `Rv`: Venous resistance <br> `Ca`: Small artery capacitance <br> `Cim`: Intramyocardial capacitance <br> `Pim`: Intramyocardial pressure <br> `Pv`: Venous pressure &emsp;

The above table describes the most commonly used boundary conditions. In addition, svZeroDSolver includes various closed-loop boundary conditions. See Menon et al. (2023) for details of a closed-loop 0D model. Examples can also be found in `svZeroDSolver/tests/cases`.

Values of the boundary condition can be specified as a function of time as follow:
```python
{
    "bc_name": "INFLOW", # Name of the boundary condition
    "bc_type": "FLOW", # Type of the boundary condition
    "bc_values": {
        "Q": [ ..., ..., ... ], # Comma-separated list of values
        "t": [ ..., ..., ... ]  # Comma-separated list of corresponding time stamps
    }
},
```
See `svZeroDSolver/tests/cases/pulsatileFlow_R_RCR.json` for an example.

### Simulation Outputs

The simulation outputs will be saved in the specified CSV file (`<name_of_output_file>.csv`) when running `svZeroDSolver` from the command line as follows:
```bash
svzerodsolver <name_of_configuration_file>.json <name_of_output_file>.csv
```
If the name of the CSV file is not specified, the default is `output.csv`. The format of the file depends on the user-specified configuration within the `simulation_parameters` block of the JSON configuration file.

If `output_variable_based` is set to `true`, the CSV file will contain all the degrees-of-freedom in the simulation. Otherwise, only the flow and pressure at the inlets and outlets of vessels is written.

The degrees-of-freedom (DOFs) follow the following naming scheme:

- Flow DOFs are labelled `flow:<name_of_upstream_block>:<name_of_downstream_block>`.
- Pressure DOFs are labelled `pressure:<name_of_upstream_block>:<name_of_downstream_block>`.
- Internal DOFs (i.e., variables internal to a block and not connected to upstream/downstream blocks) are labelled `<variable_name>:<block_name>`. The internal variables for each block are listed in the blocks' [class documentation](https://simvascular.github.io/svZeroDSolver/annotated.html).

When the outputs are written in the variable-based and vessel-based forms, the user can specify whether they want outputs written for all cardiac cycles or just the last cardiac cycle using the `output_all_cycles` option. By default, only the last cycle is written. This makes the simulation more efficient.

The number of timesteps between each time the output is written is specified by `output_interval`. By default, output is written at every time step.

## svZeroDCalibrator - Quick User Guide

svZeroDCalibrator can be used to calibrate cardiovascular 0D models (i.e. infer optimal
parameters for the 0D elements) based on a given transient result (i.e. from a
3D simulation).

### Run svZeroDCalibrator

#### From the command line
svZeroDCalibrator can be executed from the command line using a JSON configuration
file.

```bash
svzerodcalibrator path/to/input_file.json path/to/output_file.json
```

The result will be written to a JSON file.


#### In Python

svZeroDCalibrator can also be called directly from Python.
Please make sure that you installed svZerodSolver via pip to enable this feature. We start by
importing pysvzerod:

```python
import pysvzerod

my_unoptimized_config = {...}
my_optimized_config = pysvzerod.calibrate(my_unoptimized_config)
```

### Configuration file

In order to make svZeroDCalibrator easy to use, it is based on a similar configuration
file than svZeroDSolver. Instead of the `simulation_parameters` section, it has a section
called `calibration_parameters`. Additionally the optimization target (i.e. a given)
3D result is passed with the key `y` and it's temporal derivative via `dy`. See
`tests/cases/steadyFlow_calibration.json` for an example input file.

```python
{
    "calibration_parameters": {...},
    "vessels": [...],
    "junctions": [...],
    "boundary_conditions": [...],
    "y": {
      "flow:INFLOW:branch0_seg0": [0.0, 0.1, ...],  # Time series for DOF
      "pressure:INFLOW:branch0_seg0": [0.0, 0.1, ...],  # Time series for DOF
      ...
    },
    "dy": {
      "flow:INFLOW:branch0_seg0": [0.0, 0.1, ...],  # Time series for DOF
      "pressure:INFLOW:branch0_seg0": [0.0, 0.1, ...],  # Time series for DOF
      ...
    },
}
```

#### Calibration parameters

Here is a list of the parameters that can be specified in the `calibration_parameters`
section of the configuration file.

Parameter key &emsp;                      | Description &emsp;                                                     | Default value &emsp;
----------------------------------------- | ---------------------------------------------------------------------- | -----------
`tolerance_gradient` &emsp;               | Gradient tolerance for calibration &emsp;                              | $10^{-5}$ &emsp;
`tolerance_increment` &emsp;              | Increment tolerance for calibration &emsp;                             | $10^{-10}$ &emsp;
`maximum_iterations` &emsp;               | Maximum calibration iterations &emsp;                                  | 100 &emsp;
`calibrate_stenosis_coefficient` &emsp;   | Toggle whether stenosis coefficient should be calibrated &emsp;        | True &emsp;
`set_capacitance_to_zero` &emsp;          | Toggle whether all capacitances should be manually set to zero &emsp;  | False &emsp;
`initial_damping_factor` &emsp;           | Initial damping factor for Levenberg-Marquardt optimization &emsp;     | 1.0 &emsp;

## svZeroDVisualization

### About

svZeroDVisualization is a web application designed for visualizing 0D simulation results and the 0D network. It allows users to interactively explore and analyze their simulation data through an intuitive interface.
This application is available in the  `applications` folder.


### Architecture
svZeroDVisualization is built using a robust architecture that includes:
- Frontend: Utilizes HTML, CSS, Dash, and Plotly for creating a dynamic and interactive user interface. This setup allows for effective visualization and interaction with the 0D network and simulation results.
- Backend: Powered by a Flask application that handles the server-side logic. It leverages NetworkX for managing and visualizing the network graph and a Python code to determine network connections.

### Installing Dependencies

1. We recommend using a virtual environment to help manage project-specific
dependencies and avoid conflicts with other projects.
    - Using venv:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    - Using Conda:
    ```bash
    conda create --name myenv python=3.12  # Replace with your desired Python version
    conda activate myenv
    ```

2. Install the necessary packages:
    ```bash
    pysvzerod
    pandas
    matplotlib
    networkx
    dash
    plotly
    numpy
    argparse
    ```

### How to Use
Note: Files related to this application are in the `applications`folder, within the `dirgraph_visualization` subdirectory.

1. Command line execution: Pass the file path to your input JSON file and the output directory where you want the visualization to be saved as command line arguments.
    - Pass a third argument `export_csv` optionally if you want to save svZeroDSolver raw output.
    - The program will execute svZeroDSolver, generate a directed graph visualization of your network, parse simulation results, and display the results along with the corresponding nodes on a local Flask server.
    ```bash
    python applications/svZeroDVisualization/visualize_simulation.py 'tests/cases/chamber_elastance_inductor.json' './output/circuit_img/dir_graph'
    ```

2. Once the server is open, you can click on a node to inspect further.
    - The data for that node will be displayed, including the simulation parameters input for that node, pressure/flow data, and any internal variables if present.
    - Additional features include the ability to download figures and use the trace function
   for more detailed inspection of network elements. The trace feature allows users to filter the
   view by specific element types, such as isolating and examining only the blood vessels or
   identifying the locations of the chambers within the network. This functionality enhances the
   ability to focus on and analyze particular components of the network with precision.

## svZeroDGUI

### About

The svZeroDGUI application is designed to facilitate the creation of 0D model input files
through an intuitive graphical user interface. Located in the `applications` folder,
this tool allows users to generate input files for the svZeroDSolver by visually
drawing and configuring the network.

Unlike manual file creation, which can be
cumbersome and error-prone, svZeroDGUI provides an easy-to-use interface that
simplifies the process of defining network components such as vessels, junctions, and
boundary conditions. This application is especially valuable for users who lack access to
3D models or seek an efficient alternative to manual file generation, making the model creation
process both faster and more user-friendly.

### Architecture

svZeroDGUI is built using a robust architecture that includes:
* Frontend: The frontend is developed with HTML, CSS, and JavaScript to create a
responsive and user-friendly interface. It utilizes Cytoscape.js, a popular package for creating
interactive elements and graphical networks.

*  Backend: Flask app, Node.js for server-side logic, and Cypress for testing.
This architecture supports an intuitive user experience for
generating and managing 0D input files through a graphical interface.

### How to Use
1. Create a virtual environment with the required `flask` dependency. If using `conda`, use the below commands:
    ```bash
    conda create -n svZeroDGUI python=3.10 flask
    conda activate svZeroDGUI
    ```
2. Navigate to the `applications` folder and then to the `create_0dmodel` subdirectory.
3. Launch the `app.py` file.
    ```bash
    python applications/svZeroDGUI/app.py
    ```
4. Select a node type and name the node.
    - For vessels, after drawing the node, click on it to open a form
where you can enter details such as vessel length, diameter, and more.
    - For junctions, click the node to specify if it’s a Normal %Junction
or a Blood Vessel %Junction.
5. To draw edges between nodes, toggle the `Draw on` button on the right.
Once active, you can start connecting nodes by drawing edges between them.
6. When you wish to stop drawing edges and continue adding or moving nodes,
click the `Draw off` button.
7. Once you’ve completed the network, click `Export to JSON` on the right.
If there are any incorrect connections or patterns, an alert will prompt you
to make necessary changes so the network can be processed by svZeroDSolver.
8. Open the downloaded JSON file and add any additional information,
such as boundary condition data, before running it through svZeroDSolver.

## 0D Solver Theory

Flow rate, pressure, and other hemodynamic quantities in 0D models of vascular anatomies are governed by a system of nonlinear differential-algebraic equations (DAEs). In svZeroDSolver, the governing equations for a full 0D model are based on the governing equations for the individual blocks that make up the model.

### Governing equations

For each block, with $N_d^e$ degrees-of-freedom and $N_e^e$ governing equations, we represent its governing equations as the following DAE: 
$$\mathbf{E}^e(\boldsymbol{\alpha}^e) \cdot \dot{\mathbf{y}}^e + \mathbf{F}^e(\boldsymbol{\alpha}^e) \cdot \mathbf{y}^e + \mathbf{c}^e(\mathbf{y}^e,\dot{\mathbf{y}}^e, t) = \mathbf{0},$$
where $\mathbf{y}^e \in \mathbb{R}^{N_d^e}$ is the vector of unknown degrees-of-freedom, $\mathbf{c}^e \in \mathbb{R}^{N_e^e}$, $\textbf{E}^e,\textbf{F}^e \in \mathbb{R}^{N_e^e \times N_d^e}$. Here, $\boldsymbol{\alpha}^e$ represents the parameters of the specific block.

The governing equations for each block in svZeroDSolver, along with the corresponding electric circuit representation, can be found within their respective documentation pages. An overview of all the blocks is available [here](https://simvascular.github.io/svZeroDSolver/class_block.html). Below are the documentation pages for a few important blocks:

* [Blood vessel](https://simvascular.github.io/svZeroDSolver/class_blood_vessel.html)
* [Junction](https://simvascular.github.io/svZeroDSolver/class_junction.html)
* [Windkessel/RCR boundary condition](https://simvascular.github.io/svZeroDSolver/class_windkessel_b_c.html)
* [Coronary boundary condition](https://simvascular.github.io/svZeroDSolver/class_open_loop_coronary_b_c.html)
* [Cardiac chamber](https://simvascular.github.io/svZeroDSolver/class_chamber_elastance_inductor.html)
* [Valve](https://simvascular.github.io/svZeroDSolver/class_valve_tanh.html)

svZeroDSolver uses the `.json` configuration file described in the user guide to assemble the governing equations for each block (written in the form above), and the connectivity amongst the blocks, into a global set of governing equations. This is done in a similar manner to a finite element solver, where the global assembly is based on the local contributions of each block via their corresponding $\textbf{E}^e$, $\textbf{F}^e$ and $\textbf{c}^e$ matrices/vectors. 

The global governing equation is given by:
$$\mathbf{r}(\boldsymbol{\alpha}, \mathbf{y},\dot{\mathbf{y}}, t) = \mathbf{E}(\boldsymbol{\alpha}) \cdot \dot{\mathbf{y}} + \mathbf{F}(\boldsymbol{\alpha}) \cdot \mathbf{y} + \mathbf{c}(\mathbf{y},\dot{\mathbf{y}}, t) = \mathbf{0}, $$
where $\mathbf{r},\mathbf{y},\mathbf{c} \in \mathbb{R}^{N}$ and $\textbf{E},\textbf{F} \in \mathbb{R}^{N \times N}$. Here, $\mathbf{r}$ is the residual, $\mathbf{y}$ is the vector of solution quantities and $\dot{\mathbf{y}}$ is its time derivative. Note that the solution quantities are generally the pressure and flow at each node between blocks, as well as state variables internal to each block. $N$ is the total number of equations and the total number of global unknowns. 

The DAE system is solved implicitly using the generalized-$\alpha$ method (Jansen, et al., 2000). A description of this is provided in the "Time integration" section of this documentation. We then use the Newton-Raphson method to iteratively solve
$$\mathbf{K}^{i} \cdot \Delta\dot{\mathbf{y}}^{i} = - \mathbf{r}^{i}$$
with solution increment $\Delta\dot{\mathbf{y}}^{i}$ in iteration $i$. The linearization of the time-discretized system is
$$\mathbf{K} =\frac{\partial \mathbf{r}}{\partial \mathbf{y}} = c_{\dot{\mathbf{y}}} \left( \mathbf{E} + \frac{\partial \mathbf{c}}{\partial
\dot{\mathbf{y}}} \right) + c_{\mathbf{y}} \left( \mathbf{F} + \frac{\partial \mathbf{c}}{\partial \mathbf{y}} \right),$$
with time factors $c_{\dot{\mathbf{y}}}=\alpha_m$ and $c_{\mathbf{y}}=\alpha_f\gamma\Delta t$ provided by the generalized-$\alpha$ method.

The implementation of the global governing equations is in the [SparseSystem class](https://simvascular.github.io/svZeroDSolver/class_sparse_system.html). 

### Time integration

The DAE system is solved implicitly using the generalized-$\alpha$ method (Jansen, et al., 2000). The specific implementation in this solver is based on Bazilevs, et al. 2013 (Section 4.6.2).

We are interested in solving the DAE system defined above for the solutions, $\mathbf{y}_{n+1}$ and $\dot{\mathbf{y}}_{n+1}$, at the
next time, $t_{n+1}$, using the known solutions, $\mathbf y_n$ and $\dot{\mathbf y}_{n}$, at the current time, $t_n$. Note that $t_{n+1} = t_n + \Delta t$, where $\Delta t$ is the time step size.

Using the generalized-$\alpha$ method, we launch a predictor step and a series of multi-corrector steps to solve for $\mathbf{y}_{n+1}$ and $\dot{\mathbf{y}}_{n+1}$. Similar to other predictor-corrector schemes, we evaluate the solutions at intermediate times between $t_{n}$ and $t_{n + 1}$. However, in the generalized-$\alpha$ method, we evaluate $\mathbf{y}$ and $\dot{\mathbf{y}}$ at different intermediate times. Specifically, we evaluate $\mathbf{y}$ at $t_{n+\alpha_{f}}$ and $\dot{\mathbf{y}}$ at $t_{n+\alpha_{m}}$, where $t_{n+\alpha_{f}} = t_{n} + \alpha_{f}\Delta t$ and $t_{n+\alpha_{m}} = t_{n} + \alpha_{m}\Delta t$. Here, $\alpha_{m}$ and $\alpha_{f}$ are the generalized-$\alpha$ parameters, where $\alpha_{m} = \frac{3 - \rho}{2+ 2\rho}$ and $\alpha_{f} = \frac{1}{1 + \rho}$. We set the default spectral radius $\rho=0.5$, whereas $\rho=0.0$ equals the BDF2 scheme and $\rho=1.0$ equals the trapezoidal rule. For each time step $n$, the procedure works as follows.

**Predict** the new time step based on the assumption of a constant solution $\mathbf{y}$ and consistent time derivative $\dot{\mathbf{y}}$:
$$\dot{\mathbf y}_{n+1}^0 = \frac{\gamma-1}{\gamma} \dot{\mathbf y}_n,$$ 

$$\mathbf y_{n+1}^0 = \mathbf y_n.$$ 
with $\gamma = \frac{1}{2} + \alpha_m - \alpha_f$. We then iterate through Newton-Raphson iterations $i$ as follows, until the residual is smaller than an absolute error $||\mathbf r||_\infty < \epsilon_\text{abs}$:

1. **Initiate** the iterates at the intermediate time levels:

$$\dot{\mathbf y}_{n+\alpha_m}^i = \dot{\mathbf y}_n + \alpha_m \left(\dot{\mathbf y}_{n+1}^i - \dot{\mathbf y}_n  \right),$$

$$\mathbf y_{n+\alpha_f}^i= \mathbf y_n + \alpha_f \left( \mathbf y_{n+1}^i - \mathbf y_n \right).$$

2. **Solve** for the increment $\Delta\dot{\mathbf{y}}$ in the linear system:

$$\mathbf K(\mathbf y_{n+\alpha_f}^i, \dot{\mathbf y}_{n+\alpha_m}^i) \cdot \Delta \dot{\mathbf y}_{n+1}^i = - \mathbf r(\mathbf y_{n+\alpha_f}^i, \dot{\mathbf y}_{n+\alpha_m}^i).$$

3. **Update** the solution vectors:

$$\dot{\mathbf y}_{n+1}^{i+1} = \dot{\mathbf y}_{n+1}^i + \Delta \dot{\mathbf y}_{n+1}^i,$$

$$\mathbf y_{n+1}^{i+1} = \mathbf y_{n+1}^i + \Delta \dot{\mathbf y}_{n+1}^i \gamma \Delta t_n.$$


The time integration is implemented in the [Integrator class](https://simvascular.github.io/svZeroDSolver/class_integrator.html). 

## Developer guide

If you are a developer and want to contribute to svZeroDSolver, you can find more helpful information in our [Developer Guide](https://simvascular.github.io/svZeroDSolver/developer_guide.html).

## References
Relevant literature can be found [here](https://simvascular.github.io/svZeroDSolver/citelist.html).
