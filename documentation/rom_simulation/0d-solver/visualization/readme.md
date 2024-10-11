## svZeroDVisualization

### About

svZeroDVisualization is a web application designed for visualizing 0D simulation results and the 0D network. It allows users to interactively explore and analyze their simulation data through an intuitive interface.
This application is available in the  `applications` folder.

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
