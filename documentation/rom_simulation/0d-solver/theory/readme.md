## 0D Solver Theory

Flow rate, pressure, and other hemodynamic quantities in 0D models of vascular anatomies are governed by a system of nonlinear differential-algebraic equations (DAEs). In svZeroDSolver, the governing equations for a full 0D model are based on the governing equations for the individual blocks that make up the model.

### Governing Equations

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

The DAE system is solved implicitly using the generalized-$\alpha$ method (<a href="#0d-Jansen2000">Jansen, et al., 2000</a>). A description of this is provided in the <a href="#time-integration">Time Integration</a> section of this documentation. We then use the Newton-Raphson method to iteratively solve
$$\mathbf{K}^{i} \cdot \Delta\dot{\mathbf{y}}^{i} = - \mathbf{r}^{i}$$
with solution increment $\Delta\dot{\mathbf{y}}^{i}$ in iteration $i$. The linearization of the time-discretized system is
$$\mathbf{K} =\frac{\partial \mathbf{r}}{\partial \mathbf{y}} = c_{\dot{\mathbf{y}}} \left( \mathbf{E} + \frac{\partial \mathbf{c}}{\partial
\dot{\mathbf{y}}} \right) + c_{\mathbf{y}} \left( \mathbf{F} + \frac{\partial \mathbf{c}}{\partial \mathbf{y}} \right),$$
with time factors $c_{\dot{\mathbf{y}}}=\alpha_m$ and $c_{\mathbf{y}}=\alpha_f\gamma\Delta t$ provided by the generalized-$\alpha$ method.

The implementation of the global governing equations is in the [SparseSystem class](https://simvascular.github.io/svZeroDSolver/class_sparse_system.html). 

<h3 id="time-integration">Time Integration</h3>
<!--### Time integration-->

<!--For unknown reasons, need to escape (\) underscores for SOME in-line eqns from here onwards. See below:-->
<!--https://docs.mathjax.org/en/latest/input/tex/html.html#interactions-with-content-management-systems-->
<!--https://stackoverflow.com/questions/77375192/latex-equation-does-not-render-as-in-line-math-with-jekyll-and-mathjax-->

The DAE system is solved implicitly using the generalized-$\alpha$ method (<a href="#0d-Jansen2000">Jansen, et al., 2000</a>). The specific implementation in this solver is based on <a href="#0d-Bazilevs2013">Bazilevs, et al. 2013</a>(Section 4.6.2).

We are interested in solving the DAE system defined above for the solutions, $\mathbf{y}\_{n+1}$ and $\dot{\mathbf y}\_{n+1}$, at the
next time, $t\_{n+1}$, using the known solutions, $\mathbf y\_n$ and $\dot{\mathbf y}\_{n}$, at the current time, $t\_n$. Note that $t\_{n+1} = t\_n + \Delta t$, where $\Delta t$ is the time step size.

Using the generalized-$\alpha$ method, we launch a predictor step and a series of multi-corrector steps to solve for $\mathbf{y}\_{n+1}$ and $\dot{\mathbf{y}}\_{n+1}$. Similar to other predictor-corrector schemes, we evaluate the solutions at intermediate times between $t\_{n}$ and $t\_{n + 1}$. However, in the generalized-$\alpha$ method, we evaluate $\mathbf{y}$ and $\dot{\mathbf{y}}$ at different intermediate times. Specifically, we evaluate $\mathbf{y}$ at $t\_{n+\alpha_{f}}$ and $\dot{\mathbf{y}}$ at $t\_{n+\alpha_{m}}$, where $t\_{n+\alpha\_{f}} = t\_{n} + \alpha\_{f}\Delta t$ and $t\_{n+\alpha\_{m}} = t\_{n} + \alpha\_{m}\Delta t$. Here, $\alpha\_{m}$ and $\alpha\_{f}$ are the generalized-$\alpha$ parameters, where $\alpha\_{m} = \frac{3 - \rho}{2+ 2\rho}$ and $\alpha\_{f} = \frac{1}{1 + \rho}$. We set the default spectral radius $\rho=0.5$, whereas $\rho=0.0$ equals the BDF2 scheme and $\rho=1.0$ equals the trapezoidal rule. For each time step $n$, the procedure works as follows.

**Predict** the new time step based on the assumption of a constant solution $\mathbf{y}$ and consistent time derivative $\dot{\mathbf{y}}$:
$$\dot{\mathbf y}_{n+1}^0 = \frac{\gamma-1}{\gamma} \dot{\mathbf y}_n,$$ 

$$\mathbf y_{n+1}^0 = \mathbf y_n.$$ 
with $\gamma = \frac{1}{2} + \alpha_m - \alpha_f$. We then iterate through Newton-Raphson iterations $i$ as follows, until the residual is smaller than an absolute error $||\mathbf r||_\infty < \epsilon_\text{abs}$:

1. **Initiate** the iterates at the intermediate time levels:

$$\dot{\mathbf y}\_{n+\alpha\_m}^i = \dot{\mathbf y}\_n + \alpha\_m \left(\dot{\mathbf y}\_{n+1}^i - \dot{\mathbf y}\_n  \right),$$

$$\mathbf y_{n+\alpha_f}^i= \mathbf y_n + \alpha_f \left( \mathbf y_{n+1}^i - \mathbf y_n \right).$$

2. **Solve** for the increment $\Delta\dot{\mathbf{y}}$ in the linear system:

$$\mathbf K(\mathbf y\_{n+\alpha\_f}^i, \dot{\mathbf y}\_{n+\alpha\_m}^i) \cdot \Delta \dot{\mathbf y}\_{n+1}^i = - \mathbf r(\mathbf y\_{n+\alpha\_f}^i, \dot{\mathbf y}\_{n+\alpha\_m}^i).$$

3. **Update** the solution vectors:

$$\dot{\mathbf y}\_{n+1}^{i+1} = \dot{\mathbf y}\_{n+1}^i + \Delta \dot{\mathbf y}\_{n+1}^i,$$

$$\mathbf y_{n+1}^{i+1} = \mathbf y_{n+1}^i + \Delta \dot{\mathbf y}_{n+1}^i \gamma \Delta t_n.$$

The time integration is implemented in the [Integrator class](https://simvascular.github.io/svZeroDSolver/class_integrator.html). 
