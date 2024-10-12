### Input File Format

svZeroDSolver is configured using either a JSON file or a Python dictionary. JSON is a convenient file format to represent a dictionary-like object. More details can be found [here](https://stackoverflow.blog/2022/06/02/a-beginners-guide-to-json-the-data-format-for-the-internet/).

The top-level structure of both is:

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
Prescribed (transient) flow &emsp;           | FlowReferenceBC &emsp;        | `FLOW` &emsp;                | `Q`: Time-dependent flow values <br> `t`: Time steps &emsp;
Prescribed (transient) pressure &emsp;       | PressureReferenceBC &emsp;    | `PRESSURE` &emsp;            | `P`: Time-dependent pressure values <br> `t`: Time steps &emsp;
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
