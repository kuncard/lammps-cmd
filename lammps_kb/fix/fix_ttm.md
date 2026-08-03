---
id: fix_ttm
title: "fix ttm command"
url: https://docs.lammps.org/fix_ttm.html
---

# fix ttm command

## Syntax

```
fix ID group-ID ttm seed C_e rho_e kappa_e gamma_p gamma_s v_0 Nx Ny Nz keyword value ...
fix ID group-ID ttm/mod seed init_file Nx Ny Nz keyword value ...
fix ID group-ID ttm/thermal seed properties_file Nx Ny Nz keyword value ...
C_e  = electronic specific heat (energy/(electron*temperature) units)
rho_e = electronic density (electrons/volume units)
kappa_e = electronic thermal conductivity (energy/(time*distance*temperature) units)
gamma_p = friction coefficient due to electron-ion interactions (mass/time units)
gamma_s = friction coefficient due to electronic stopping (mass/time units)
v_0 = electronic stopping critical velocity (velocity units)
Nx = number of thermal solve grid points in the x-direction (positive integer)
Ny = number of thermal solve grid points in the y-direction (positive integer)
Nz = number of thermal solve grid points in the z-direction (positive integer)
init_file = file with the parameters to TTM
Nx = number of thermal solve grid points in the x-direction (positive integer)
Ny = number of thermal solve grid points in the y-direction (positive integer)
Nz = number of thermal solve grid points in the z-direction (positive integer)
properties_file = file with grid based TTM properties
Nx = number of thermal solve grid points in the x-direction (positive integer)
Ny = number of thermal solve grid points in the y-direction (positive integer)
Nz = number of thermal solve grid points in the z-direction (positive integer)
set value = Tinit
  Tinit = initial electronic temperature at all grid points (temperature units)
infile value = file.in with grid values for electronic temperatures
outfile values = Nout file.out
  Nout = dump grid temperatures every this many timesteps
  file.out = filename to write grid temperatures to
source value = source
  source = volumetric heating term applied to electrons (energy/(time*volume) units)
```

## Description

Use a two-temperature model (TTM) to represent heat transfer through
and between electronic and atomic subsystems.  LAMMPS models the
atomic subsystem as usual with a molecular dynamics model and the
classical force field specified by the user.  The electronic subsystem
is modeled as a continuum, or a background  gas , on a regular grid
which overlays the simulation domain.  Energy can be transferred
spatially within the grid representing the electrons.  Energy can also
be transferred between the electronic and atomic subsystems.  The
algorithm underlying this fix was derived by D. M.  Duffy
and A. M. Rutherford and is discussed in two J Physics: Condensed
Matter papers: (Duffy) and (Rutherford).  They used this algorithm in cascade simulations where
a primary knock-on atom (PKA) was initialized with a high velocity to
simulate a radiation event.

The description in this subsection applies to all 4 fix styles:
ttm, ttm/grid, ttm/mod, and ttm/thermal.

Fix ttm/grid distributes the regular grid across processors consistent
with the subdomains of atoms owned by each processor, but is otherwise
identical to fix ttm.  Note that fix ttm stores a copy of the grid on
each processor, which is acceptable when the overall grid is reasonably
small.  For larger grids you should use fix ttm/grid instead.

Fix ttm/mod adds options to account for external heat sources (e.g. at
a surface) and for specifying parameters that allow the electronic heat
capacity to depend strongly on electronic temperature.  It is more
expensive computationally than fix ttm because it treats the thermal
diffusion equation as non-linear.  More details on fix ttm/mod are
given below.

Added in version 10Dec2025.

Fix ttm/thermal allows for electronic properties to be assigned
independently to each TTM grid point and supports external heat sources
to the electronic subsystem. More details on fix ttm/thermal are
given below.

Heat transfer between the electronic and atomic subsystems is carried
out via an inhomogeneous Langevin thermostat.  Only atoms in the fix
group contribute to and are affected by this heat transfer.

This thermostatting differs from the regular Langevin thermostat
(fix langevin) in three important ways.  First,
the Langevin thermostat is applied uniformly to all atoms in the
user-specified group for a single target temperature, whereas the TTM
fixes apply Langevin thermostatting locally to atoms within the
volumes represented by the user-specified grid points with a target
temperature specific to that grid point.  Second, the Langevin
thermostat couples the temperature of the atoms to an infinite heat
reservoir, whereas the heat reservoir for the TTM fixes is finite and
represents the local electrons.  Third, the TTM fixes allow users to
specify not just one friction coefficient, but rather two independent
friction coefficients: one for the electron-ion interactions
(gamma_p), and one for electron stopping (gamma_s).

When the friction coefficient due to electron stopping, gamma_s, is
non-zero, electron stopping effects are included for atoms moving
faster than the electron stopping critical velocity, v_0.  For
further details about this algorithm, see (Duffy) and
(Rutherford).

Energy transport within the electronic subsystem is solved according
to the heat diffusion equation with added source terms for heat
transfer between the subsystems:

\[C_e \rho_e \frac{\partial T_e}{\partial t} =
\bigtriangledown (\kappa_e \bigtriangledown T_e) -
g_p (T_e - T_a) + g_s T_a'\]

where \(C_e\) is the specific heat, \(\rho_e\) is the density,
\(\kappa_e\) is the thermal conductivity, T is temperature, the
 e  and  a  subscripts represent electronic and atomic subsystems
respectively, \(g_p\) is the coupling constant for the electron-ion
interaction, and \(g_s\) is the electron stopping coupling
parameter.  \(C_e\), \(\rho_e\), and \(\kappa_e\) are
specified as parameters to the fix ttm or ttm/grid.  The other
quantities are derived.  The form of the heat diffusion equation used
here is almost the same as that in equation 6 of (Duffy),
with the exception that the electronic density is explicitly
represented, rather than being part of the specific heat parameter.

Currently, the TTM fixes assume that none of the user-supplied
parameters will vary with temperature. Note that (Duffy)
used a tanh() functional form for the temperature dependence of the
electronic specific heat, but ignored temperature dependencies of any of
the other parameters.  See more discussion below for fix ttm/mod.

Note
These fixes do not perform time integration of the atoms in the fix
group, they only rescale their velocities.  Thus a time integration
fix such as fix nve should be used in conjunction
with these fixes.  These fixes should not normally be used on atoms
that have their temperature controlled by another thermostatting
fix, e.g. fix nvt or fix langevin.

Note
These fixes require use of an orthogonal 3d simulation box with
periodic boundary conditions in all dimensions.  They also require
that the size and shape of the simulation box do not vary
dynamically, e.g. due to use of the fix npt command.
Likewise, the size/shape of processor subdomains cannot vary due to
dynamic load-balancing via use of the fix balance command.  It is possible however to load balance
before the simulation starts using the balance
command, so that each processor has a different size subdomain.

Periodic boundary conditions are also used in the heat equation solve
for the electronic subsystem.  This varies from the approach of
(Rutherford) where the atomic subsystem was
embedded within a larger continuum representation of the electronic
subsystem.

The set keyword specifies a Tinit temperature value to initialize
the value stored on all grid points.  By default the temperatures
are all zero when the grid is created.

The infile keyword specifies an input file of electronic temperatures
for each grid point to be read in to initialize the grid, as an alternative
to using the set keyword.

The input file is a text file which may have comments starting with
the  #  character.  Each line contains four numeric columns:
ix,iy,iz,Temperature.  Empty or comment-only lines will be
ignored. The number of lines must be equal to the number of
user-specified grid points (Nx by Ny by Nz).  The ix,iy,iz are grid
point indices ranging from 1 to Nxyz inclusive in each dimension.  The
lines can appear in any order.  For example, the initial electronic
temperatures on a 1 by 2 by 3 grid could be specified in the file as
follows:

# UNITS: metal COMMENT: initial electron temperature
1 1 1 1.0
1 1 2 1.0
1 1 3 1.0
1 2 1 2.0
1 2 2 2.0
1 2 3 2.0

where the electronic temperatures along the y=0 plane have been set to
1.0, and the electronic temperatures along the y=1 plane have been set
to 2.0.  If all the grid point values are not specified, LAMMPS will
generate an error. LAMMPS will check if a  UNITS:  tag is in the first
line and stop with an error, if there is a mismatch with the current
units used.

Note
The electronic temperature at each grid point must be a non-zero
positive value, both initially, and as the temperature evolves over
time.  Thus you must use either the set or infile keyword or be
restarting a simulation that used this fix previously.

The outfile keyword has 2 values.  The first value Nout triggers
output of the electronic temperatures for each grid point every Nout
timesteps.  The second value is the filename for output, which will be
suffixed by the timestep.  The format of each output file is exactly
the same as the input temperature file. It will contain a comment in
the first line reporting the date the file was created, the LAMMPS
units setting in use, grid size and the current timestep.

Note
The fix ttm/grid command does not support the outfile keyword.
Instead you can use the dump grid command to output
the electronic temperature on the distributed grid to a dump file or
the restart command which creates a file specific
to this fix which the read restart command
reads.  The file has the same format as the file the infile option
reads.

For the fix ttm, fix ttm/mod, and fix ttm/thermal commands, the
corresponding atomic temperature for atoms in each grid cell can be
computed and output by the fix ave/chunk command
using the compute chunk/atom command to
create a 3d array of chunks consistent with the grid used by this fix.

For the fix ttm/grid command the same thing can be done using the
fix ave/grid command and its per-grid values can
be output via the dump grid command.

Additional details for fix ttm/mod

Fix ttm/mod uses the heat diffusion equation with possible external
heat sources (e.g. laser heating in ablation simulations):

\[C_e \rho_e \frac{\partial T_e}{\partial t} =
\bigtriangledown (\kappa_e \bigtriangledown T_e) -
g_p (T_e - T_a) + g_s T_a' + \theta (x-x_{surface})I_0 \exp(-x/l_{skin})\]

where \(\theta\) is the Heaviside step function, \(I_0\) is the
(absorbed) laser pulse intensity for ablation simulations,
\(l_{skin}\) is the depth of the skin-layer, and all other
designations have the same meaning as in the former equation. The
duration of the pulse is set by the parameter tau in the init_file.

Fix ttm/mod also allows users to specify the dependencies of
\(C_e\) and \(\kappa_e\) on the electronic temperature. The
specific heat is expressed as

\[C_e = C_0 + (a_0 + a_1 X + a_2 X^2 + a_3 X^3 + a_4 X^4) \exp (-(AX)^2)\]

where \(X = \frac{T_e}{1000}\), and the thermal conductivity is
defined as \(\kappa_e = D_e \cdot rho_e \cdot C_e\), where
\(D_e\) is the thermal diffusion coefficient.

Electronic pressure effects are included in the TTM model to account for
the blast force acting on ions because of electronic pressure gradient
(see (Chen), (Norman)).  The total force
acting on an ion is:

\[{\vec F}_i = - \partial U / \partial {\vec r}_i + {\vec
F}_{langevin} - \nabla P_e/n_{ion}\]

where \(F_{langevin}\) is a force from Langevin thermostat
simulating electron-phonon coupling, and \(\nabla P_e/n_{ion}\) is
the electron blast force.

The electronic pressure is taken to be \(P_e = B \cdot rho_e \cdot
C_e \cdot T_e\)

The current fix ttm/mod implementation allows TTM simulations with a
vacuum. The vacuum region is defined as the grid cells with zero
electronic temperature. The numerical scheme does not allow energy
exchange with such cells. Since the material can expand to previously
unoccupied region in some simulations, the vacuum border can be allowed
to move. It is controlled by the surface_movement parameter in the
init_file. If it is set to 1, then  vacuum  cells can be changed to
 electron-filled  cells with the temperature T_e_min if atoms move
into them (currently only implemented for the case of 1-dimensional
motion of a flat surface normal to the X axis). The initial locations of
the interfaces of the electron density to the vacuum can be set in the
init_file via lsurface and rsurface parameters. In this case,
electronic pressure gradient is calculated as

\[\nabla_x P_e = \left[\frac{C_e{}T_e(x)\lambda}{(x+\lambda)^2} +
\frac{x}{x+\lambda}\frac{(C_e{}T_e)_{x+\Delta
x}-(C_e{}T_e)_{x}}{\Delta x} \right]\]

where \(\lambda\) is the electron mean free path (see (Norman), (Pisarev))

Note
The lsurface and rsurface parameters always define the range of
electronic grid cells in the x-direction over which the electron-ion
(Langevin) coupling and any external (laser) source term are applied,
regardless of the surface_movement setting.  Only atoms in grid
cells whose x grid index ix satisfies lsurface <= ix <
rsurface are coupled to the electronic subsystem; atoms in cells
outside this range exchange no energy with the electrons.  Therefore,
to model a bulk system with full periodicity and no vacuum (i.e. to
reproduce the behavior of fix ttm), you must set lsurface = 0 and
rsurface = Nx so that the coupling acts on the entire simulation
box.  Setting rsurface to a smaller value couples only a sub-slab of
the grid cells and will make energy transfer between the two
subsystems appear much too slow.  Fix ttm/mod prints a warning when
this coupling region does not span the whole box (with
surface_movement disabled).

The fix ttm/mod parameter file init_file has the following syntax.
Every line with an odd number is considered as a comment and
ignored. The lines with the even numbers are treated as follows:

```
a_0, energy/(temperature*electron) units
a_1, energy/(temperature^2*electron) units
a_2, energy/(temperature^3*electron) units
a_3, energy/(temperature^4*electron) units
a_4, energy/(temperature^5*electron) units
C_0, energy/(temperature*electron) units
A, 1/temperature units
rho_e, electrons/volume units
D_e, length^2/time units
gamma_p, mass/time units
gamma_s, mass/time units
v_0, length/time units
I_0, energy/(time*length^2) units
lsurface, lower x grid index of the coupled (electron) region (positive integer; see note above)
rsurface, upper x grid index of the coupled (electron) region (positive integer; see note above)
l_skin, electron grid units (positive integer)
tau, time units
B, dimensionless
lambda, length units
n_ion, ions/volume units
surface_movement: 0 to disable tracking of surface motion, 1 to enable
T_e_min, temperature units
```

Additional details for fix ttm/thermal

Fix ttm/thermal uses the heat diffusion equation with possible external
heat sources (e.g. inductive heating). The effects of electron stopping
have been removed:

\[C_\mathrm{vol} \frac{\partial T_e}{\partial t} =
\bigtriangledown (\kappa_\mathrm{eff} \bigtriangledown T_e) -
g_p (T_e - T_a) + \eta s\]

where \(s\) is the applied heating power density and \(\eta\) is
the absorption efficiency (0-1) defined for each ttm grid cell in the
properties.in file. Also note that compared to the original fix ttm,
it uses use a volumetric specific heat, \(C_\mathrm{vol}\) , which
represents the product of \(C_e \rho_e\).

(Baer) defined \(\kappa_\mathrm{eff}\) as an effective
electronic thermal conductivity when two adjacent TTM cells (denoted by
the subscripts a and b) have different conductivities as:

\[\kappa_\mathrm{eff} = \frac{2 \kappa_a \kappa_b}{\kappa_a + \kappa_b}\]

The current fix ttm/thermal implementation allows TTM simulations with
TTM cells that do not contain electrons (vacuum or insulators). Similar
to ttm/mod, the absence of electrons is defined as the grid cells with
zero electronic temperature.The numerical scheme does not allow energy
exchange with such cells.

The fix ttm/thermal parameter file properties_file uses a similar syntax
as the keyword infile. The file is read in line by line and each ttm cell s
properties are set. Comment lines are allowed and each line should have
properties listed in the order:

ix iy iz C_vol kappa_e gamma_p eta

the grid must match the one declared in the fix and all grid points must have
all properties set or ttm/thermal will exit with an error.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 2 all ttm 699489 1.0 1.0 10 0.1 0.0 2.0 1 12 1 infile initial outfile 1000 T.out
fix 3 all ttm/grid 123456 1.0 1.0 1.0 1.0 1.0 5.0 5 5 5 infile Te.in
fix 4 all ttm/mod 34277 parameters.txt 5 5 5 infile T_init outfile 10 T_out
fix 5 all ttm/thermal 11111 properties.in 10 10 10 source 0.1 infile temps.in outfile 10 temps.out
```

## Restrictions

Restrictions 
All these fixes are part of the EXTRA-FIX package. They are only
enabled if LAMMPS was built with that package.  See the Build
package page for more info.
As mentioned above, these fixes require 3d simulations and orthogonal
simulation boxes periodic in all 3 dimensions.
These fixes used a random number generator to Langevin thermostat the
electron temperature.  This means you will not get identical answers
when running on different numbers of processors or when restarting a
simulation (even on the same number of processors).  However, in a
statistical sense, simulations on different processor counts and
restarted simulation should produce results which are statistically
the same.

## Related Commands

- [fix langevin](fix_langevin.html)
- [fix dt/reset](fix_dt_reset.html)

