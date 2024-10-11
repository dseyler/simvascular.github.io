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
