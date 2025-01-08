<!-- =============================================================== -->
<!-- ============== Precomputed Solution Section =================== -->
<!-- =============================================================== -->

<h2 id="precomputed_solution_section"> Precomputed Solution Section </h2>
The <i>Precomputed Solution Section</i> of the solver parameters input file is used to define the parameters 
used to read in the data from a precomputed solution for the simulation state.

A <i>Precomputed Solution Section</i> is organized as follows 
<div style="background-color: #F0F0F0; padding: 10px; border: 1px solid #d0d0d0; border-left: 1px solid #d0d0d0">
&lt;<strong>Precomputed_solution</strong>&gt; 
<br>
[ <a href="#precomputed_solution_parameters"> Precomputed Solution Parameters </a> ]
<br>
&lt;<strong>/Precomputed_solution</strong>&gt;
</div>

The <strong>Precomputed_solution</strong> keyword is used to define the parameters to for reading in a precomputed solution data and using it in a simulation. 

<h3 id= "precomputed_solution_parameters"> Precomputed Solution Parameters </h3>
<div class="bc_param_div">
<strong>&lt;Use_precomputed_solution></strong> <i>bool</i> [<i>false</i>] <nobr>
<strong>&lt;/Use_precomputed_solution&gt;</strong>
</nobr><br>
If <i>true</i> then use a precomputed solution for a simulation.
<br>
<strong>&lt;Precomputed_solution_field_name></strong> <i>string</i> [none] <nobr>
<strong>&lt;/Precomputed_solution_field_name&gt;</strong>
</nobr><br>
The name of the precomputed solution data field in the VTK VTU file.
<br>
<strong>&lt;Precomputed_solution_file_path></strong> <i>string</i> [none] <nobr>
<strong>&lt;/Precomputed_solution_file_path&gt;</strong>
</nobr><br>
The path to the VTK VTU file containing the precomputed solution data.
<br>
<strong>&lt;Precomputed_time_step_size></strong> <i>real</i> [0.05] <nobr>
<strong>&lt;/Precomputed_time_step_size&gt;</strong>
</nobr><br>
The time step used to compute the precomputed solution data.
<br>
</div>

