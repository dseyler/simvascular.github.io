# Python script to calculate lumen volume and fluid pressure on endo surface from 
# results of svFSI struct
# 
# Requires two meshes
# - svFSI result.vtu (with Displacement array)
# - reference surface file (polygonal mesh), representing the undeformed surface
#   corresponding to the deformed surface of which we want to compute the volume
#
# We calculate the volume in the following steps
# 1) Sample the result.vtu file onto the reference surface
# 2) Warp the samples surface by the Displacement
# 3) Flat fill any holes in the warped surface
# 4) Calculate the volume of the warped and filled surface
#
# We calculate the fluid pressure on the endo surface by reading the input file
# and pressure load file.

import os # for checking and creating directories, and loading modules
import matplotlib.pyplot as plt
import numpy as np
import sys

# Import custom functions useful for post-processing
from post_processing_functions import *

## -------- PARAMETERS TO CHANGE -------------------- ##

# Simulation folder file path
sim_folder = os.path.dirname(os.path.realpath(__file__))

# Optionally read sim_folder as command line argument
if len(sys.argv) == 2:
    print(sys.argv)
    sim_folder = os.path.abspath(sys.argv[1])
    print(sim_folder)


# Undeformed surface, corresponding to deformed surface on result.vtu of which we want to compute the volume
reference_surface = os.path.join(sim_folder, 'mesh/mesh-surfaces/endo.vtp')

# Undeformed vtu file (the original volume mesh)
reference_volume = os.path.join(sim_folder, 'mesh/mesh-complete.mesh.vtu')

# svFSI results folder, containing results.vtu
#results_folder = os.path.join(sim_folder, 'results_svfsi/')
results_folder = os.path.join(sim_folder, 'results/')

# File containing genBC output
#alldata_file = 'AllData_svfsi_vvedula22'
alldata_file = 'AllData'

# Input file path
input_file = os.path.join(sim_folder, 'solver.xml')

# Pressure file
pressure_dat_file = os.path.join(sim_folder, 'pressure.dat')


## -------------------- END PARAMETERS TO CHANGE ------------------------ ## 


# Automatically determine the start time, end time, and step size based on all
# results file in results_folder
print(results_folder)
(start_time, end_time, step) = get_start_end_step(results_folder)
# Option to manually set start time, end time, and time step of results files to process
#start_time = 5
#end_time = 85
#step = 5

# Compute lumen volume from simulation results
(t_3D, vol_3D) = calc_volume_struct(start_time, end_time, step, results_folder, reference_surface)
vol_3D_cm3 = np.array(vol_3D) * (100)**3 # cm^3

# Compute lumen dVdt from simulation results
(t_dVdt_3D, dVdt_3D) = calc_dVdt_struct(start_time, end_time, step, results_folder, reference_surface)
# Convert volume to cm^3/s
dVdt_3D = np.array(dVdt_3D) # cm/s * m^2
dVdt_3D_cm3 = dVdt_3D * (100)**2 # cm^3/s

# Compute lumen pressure at iterations in t
pressure = calc_pressure_struct(os.path.join(sim_folder, "solver.xml"), os.path.join(sim_folder, "pressure.dat"), t_3D) # dynes/cm^2

# Convert pressure from dynes/cm^2 to mmHg
pressure_mmHg = pressure * 0.000750062

# Plot pressure vs. volume
fig, ax = plt.subplots()
ax.plot(vol_3D_cm3, pressure_mmHg, linewidth=2.0, marker = 'o')
ax.set_xlabel('Volume [cm^3]')
ax.set_ylabel('Pressure [dyne/cm^2]')
#plt.xlim([0,0.4])
#plt.ylim([-2, 14])
plt.savefig(os.path.join(sim_folder, 'pv_plot'), bbox_inches='tight')


# Plot dVdt vs. time
fig, ax = plt.subplots()
ax.plot(t_dVdt_3D, dVdt_3D, linewidth=2.0, marker = 'o')
ax.set_xlabel('Time [s]')
ax.set_ylabel('dVdt [cm^3/s]')
#plt.xlim([0,0.4])
#plt.ylim([-2, 14])
plt.savefig(os.path.join(sim_folder, 'dVdt_plot'))
