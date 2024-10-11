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

The option `use_cycle_to_cycle_error` allows the solver to change the number of cardiac cycles it runs depending on the cycle-to-cycle convergence of the simulation. For simulations with no RCR boundary conditions, the simulation will add extra cardiac cycles until the difference between the mean pressure and flow in consecutive cycles is below the threshold set by `sim_cycle_to_cycle_percent_error` at all inlets and outlets of the model. If there is at least one RCR boundary condition, the number of cycles is determined based on equation 21 of <a href="#0d-Pfaller2021">Pfaller et al. (2021)</a>, using the RCR boundary condition with the largest time constant.


<style>
table{
    border-collapse: collapse;
    border-spacing: 100000px;
    border:1px solid #000000;
}

th{
    border:0.1px dotted #000000;
    padding: 15px;
}

td{
    border:0.1px dotted #000000;
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
------------------------------------- | ---------------------- | --------------------- | ----------
Prescribed (transient) flow &emsp;           | FlowReferenceBC &emsp;        | `FLOW` &emsp;                | `Q`: Time-dependent flow values <br> `t`: Time steps <br> `fn`: Mathematical expression <br> Note: Either specify `Q` and `t` together, or just `fn` &emsp;
Prescribed (transient) pressure &emsp;       | PressureReferenceBC &emsp;    | `PRESSURE` &emsp;            | `P`: Time-dependent pressure values <br> `t`: Time steps <br> `fn`: Mathematical expression <br> Note: Either specify `Q` and `t` together, or just `fn` &emsp;
Resistance &emsp;                            | ResistanceBC &emsp;           | `RESISTANCE` &emsp;          | `R`: Resistance <br> `Pd`: Time-dependent distal pressure <br> `t`: Time stamps &emsp;
Windkessel or RCR &emsp;                            | WindkesselBC &emsp;           | `RCR` &emsp;                 | `Rp`: Proximal resistance <br> `C`: Capacitance <br> `Rd`: Distal resistance <br> `Pd`: Distal pressure &emsp;
Coronary outlet &emsp;                       | OpenLoopCoronaryBC &emsp;     | `CORONARY` &emsp;            | `Ra`: Proximal resistance <br> `Ram`: Microvascular resistance <br> `Rv`: Venous resistance <br> `Ca`: Small artery capacitance <br> `Cim`: Intramyocardial capacitance <br> `Pim`: Intramyocardial pressure <br> `Pv`: Venous pressure &emsp;

The above table describes the most commonly used boundary conditions. In addition, svZeroDSolver includes various closed-loop boundary conditions. See <a href="#0d-Menon2023">Menon et al. (2023)</a> for details of a closed-loop 0D model. Examples can also be found in `svZeroDSolver/tests/cases`.

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
