<!-- --------------------------------------------- -->
<!-- ----------- Cardiac Mechanics Example -------- -->
<!-- --------------------------------------------- -->

<h3> Cardiac Mechanics Example </h3>

Solving cardiac mechanics is a challenging task as the myocardium is a complex fibrous structure that is predominantly incompressible and undergoes large deformation during a cardiac cycle. In the following sections, we introduce the workflow of modeling cardiac mechanics in **svMultiPhysics** using a benchmark example for the active contraction of an idealized left ventricle.

<h4> Input Files </h4>

<b>Geometry meshes:</b> Three surface meshes (<code>base.vtp</code>, <code>endo.vtp</code>, <code>epi.vtp</code>) are provided, representing the basal, endocardial, and epicardial surfaces respectively. A 3D volume mesh (<code>mesh-complete.vtu</code>) is also included. These meshes are provided for this example but can also be generated and labeled for any arbitrary geometry using SimVascular’s GUI.

<b>Fiber meshes:</b> The myocardium is a composite of layers (or sheets) of parallel cardiomyocytes. **svMultiPhysics** takes two fiber meshes as inputs:

<ul>
  <li><code>FibersLong.vtu</code>: specifies the longitudinal axis direction of cardiomyocytes at the centroid of each element (active contraction direction).</li>
  <li><code>FibersSheet.vtu</code>: specifies the sheet direction (orthogonal to <code>FibersLong.vtu</code>).</li>
</ul>

These meshes must contain a vector field named <code>FIB_DIR</code>. In this example, the two fiber meshes are provided, but they could alternatively be generated using a rule-based method.

<b>Active stress and pressure data:</b> The files <code>stress.dat</code> and <code>pressure.dat</code> contain temporal data for active stress and endocardial pressure, respectively. The format includes:

<ul>
  <li>Row 1, column 1: number of timesteps</li>
  <li>Following rows, column 1: time (s)</li>
  <li>Row 1, column 2: number of Fourier modes</li>
  <li>Following rows, column 2: stress/pressure values</li>
</ul>

<h4> Running the Simulation </h4>

Below is the input file for this simulation with explanations of each section.

<h4> General Simulation Parameters </h4>

The first section defines the general simulation parameters, including the number of spatial dimensions, number of time steps, spectral radius to ensure numerical stability, and information on where and how often to save results.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<svMultiPhysicsFile version="0.1">

<GeneralSimulationParameters>
  <Continue_previous_simulation> 0 </Continue_previous_simulation>
  <Number_of_spatial_dimensions> 3 </Number_of_spatial_dimensions> 
  <Number_of_time_steps> 1000 </Number_of_time_steps> 
  <Time_step_size> 1e-3 </Time_step_size> 
  <Spectral_radius_of_infinite_time_step> 0.50 </Spectral_radius_of_infinite_time_step> 
  <Searched_file_name_to_trigger_stop> STOP_SIM </Searched_file_name_to_trigger_stop> 

  <Save_results_to_VTK_format> 1 </Save_results_to_VTK_format> 
  <Name_prefix_of_saved_VTK_files> result </Name_prefix_of_saved_VTK_files> 
  <Save_results_in_folder> results </Save_results_in_folder>
  <Increment_in_saving_VTK_files> 10 </Increment_in_saving_VTK_files> 
  <Start_saving_after_time_step> 1 </Start_saving_after_time_step> 

  <Increment_in_saving_restart_files> 50 </Increment_in_saving_restart_files> 
  <Convert_BIN_to_VTK_format> 0 </Convert_BIN_to_VTK_format> 

  <Verbose> 1 </Verbose> 
  <Warning> 1 </Warning> 
  <Debug> 1 </Debug> 

</GeneralSimulationParameters>
```

<h4> Mesh Definition </h4>

<p>The next section defines the path to each surface, volume, and fiber meshes, as well as the name they will be referred to as later in the input file. A mesh scale factor is also included because the mesh is in SI units while the simulation parameters are in CGS units. Alternatively, the simulation parameters could have been given in SI units with no scaling factor.</p>

```xml
<Add_mesh name="msh">
  <Mesh_file_path> mesh/mesh-complete.mesh.vtu </Mesh_file_path>

  <Add_face name="endo">
    <Face_file_path> mesh/mesh-surfaces/endo.vtp </Face_file_path>
  </Add_face>

  <Add_face name="epi">
    <Face_file_path> mesh/mesh-surfaces/epi.vtp </Face_file_path>
  </Add_face>

  <Add_face name="base">
    <Face_file_path> mesh/mesh-surfaces/base.vtp </Face_file_path>
  </Add_face>

  <Fiber_direction_file_path> mesh/fibersLong.vtu </Fiber_direction_file_path>
  <Fiber_direction_file_path> mesh/fibersSheet.vtu </Fiber_direction_file_path>

  <Mesh_scale_factor> 100.0 </Mesh_scale_factor>
</Add_mesh>
```

<h4> Equation and Material Model Setup </h4>

<p>Next, the input file defines the equation type to be solved as well as the linear solver parameters. Here, we are simulating the nonlinear structural dynamics problem using a formulation based on velocity and pressure (ustruct).</p>

<p>The material properties for the mesh are also described in this section. We use a poisson ratio of 0.483333 as a poisson ratio too close to 0.5 can introduce numerical instabilities. In this example, we use the Holzapfel-Ogden modified anisotropy constitutive model which models the behavior of anisotropic, fibrous, soft biological tissues.</p>

<p>The solver performs a minimum of 6 and a maximum of 10 nonlinear iterations per timestep with a tolerance of 1e-9 using the Newton-Raphson method. Within each nonlinear iteration, a GMRES linear solver is used along with an FSILS preconditioner. The linear solver has a tolerance of 1e-9 and a maximum of 1000 linear iterations for per nonlinear iteration.</p>

```xml
<Add_equation type="ustruct">
  <Coupled> true </Coupled>
  <Min_iterations> 6 </Min_iterations>
  <Max_iterations> 10 </Max_iterations>
  <Tolerance> 1e-9 </Tolerance>

  <Density> 1.0 </Density>
  <Elasticity_modulus> 1.0e6 </Elasticity_modulus>
  <Poisson_ratio> 0.483333 </Poisson_ratio>

  <Viscosity model="Potential">
    <Value> 1000.0 </Value>
  </Viscosity>

  <Constitutive_model type="HolzapfelOgden-ModifiedAnisotropy">
    <a> 590.0 </a>
    <b> 8.023 </b>
    <a4f> 184720.0 </a4f>
    <b4f> 16.026 </b4f>
    <a4s> 24810.0 </a4s>
    <b4s> 11.12 </b4s>
    <afs> 2160.0 </afs>
    <bfs> 11.436 </bfs>
    <k> 100.0 </k>
  </Constitutive_model>

  <Dilational_penalty_model> ST91 </Dilational_penalty_model>
  <Penalty_parameter> 1e7 </Penalty_parameter>

  <Momentum_stabilization_coefficient> 1e-5 </Momentum_stabilization_coefficient>
  <Continuity_stabilization_coefficient> 1e-5 </Continuity_stabilization_coefficient>

  <Fiber_reinforcement_stress type="Unsteady">
    <Temporal_values_file_path> stress.dat </Temporal_values_file_path>
    <Ramp_function> false </Ramp_function>
  </Fiber_reinforcement_stress>

  <Output type="Spatial">
    <Displacement> true </Displacement>
    <Velocity> true </Velocity>
    <Jacobian> true </Jacobian>
    <Stress> true </Stress>
    <Strain> true </Strain>
    <VonMises_stress> true </VonMises_stress>
  </Output>

  <LS type="GMRES">
    <Linear_algebra type="fsils">
      <Preconditioner> fsils </Preconditioner>
    </Linear_algebra>
    <Tolerance> 1e-9 </Tolerance>
    <Max_iterations> 1000 </Max_iterations>
    <Krylov_space_dimension> 50 </Krylov_space_dimension>
  </LS>
```

<h4> Boundary Conditions </h4>
<p>Finally, the boundary conditions on each surface are defined. We use Robin boundary conditions on the basal and epicardial surface to model the resistance of the pericardium and other surrounding tissue. The supplied temporal pressure values are prescribed as a Neumann boundary condition on the endocardial surface.</p>


```xml
  <Add_BC name="epi">
    <Type> Robin </Type>
    <Stiffness> 1.0e7 </Stiffness>
    <Damping> 5.0e2 </Damping>
    <Apply_along_normal_direction> 1 </Apply_along_normal_direction>
  </Add_BC>

  <Add_BC name="base">
    <Type> Robin </Type>
    <Stiffness> 1.0e4 </Stiffness>
    <Damping> 5.0e2 </Damping>
  </Add_BC>

  <Add_BC name="endo">
    <Type> Neu </Type>
    <Time_dependence> Unsteady </Time_dependence>
    <Temporal_values_file_path> pressure.dat </Temporal_values_file_path>
    <Ramp_function> false </Ramp_function>
    <Follower_pressure_load> true </Follower_pressure_load>
  </Add_BC>

</Add_equation>

</svMultiPhysicsFile>
```


