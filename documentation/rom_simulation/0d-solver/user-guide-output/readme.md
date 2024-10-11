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
