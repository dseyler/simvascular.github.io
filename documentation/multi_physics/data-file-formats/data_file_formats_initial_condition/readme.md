
<h2 id="data_file_formats_initial_condition"> Initial Condition Data</h2>
Initial condition data for a finite element volume mesh can be initialized from values contained in a 
<a href="#appendix_vtk_file_format"> VTK VTU </a> format file containing PointData arrays.

<h3> Displacement, Pressure, Stress, and Velocity Data</h3>
Displacement, pressure, stress, and velocity data can be initialized using <a href="#appendix_vtk_file_format"> VTK VTU </a> 
format file containing PointData arrays named <strong>Displacement</strong>, <strong>Pressure</strong>, <strong>Stress</strong>, and <strong>Velocity</strong>. 

The data files are set using the solver input file 
<a href="#mesh_params_Initial_displacements_file_path"> Initial_displacements_file_path</a>, 
<a href="#mesh_params_Initial_pressures_file_path"> Initial_pressures_file_path</a> and 
<a href="#mesh_params_Prestress_file_path"> Prestress_file_path </a> and 
<a href="#mesh_params_Initial_velocities_file_path"> Initial_velocities_file_path</a> keywords.

<h3> State Variables </h3>
All state variables for a simulation can be initialized using <a href="#appendix_vtk_file_format"> VTK VTU </a> 
format file containing the appropriate PointData arrays.

The data file is set using the solver input file 
<a href="#general_params_Simulation_initialization_file_path"> Simulation_initialization_file_path</a> keyword.

