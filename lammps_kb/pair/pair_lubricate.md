---
id: pair_lubricate
title: "pair_style lubricate command"
url: https://docs.lammps.org/pair_lubricate.html
---

# pair_style lubricate command

## Syntax

```
pair_style style mu flaglog flagfld cutinner cutoff flagHI flagVF
```

## Description

Styles lubricate and lubricate/poly compute hydrodynamic
interactions between mono-disperse finite-size spherical particles in
a pairwise fashion.  The interactions have 2 components.  The first is
Ball-Melrose lubrication terms via the formulas in (Ball and Melrose)

\[\begin{split}W & =  - a_{sq} | (v_1 - v_2) \bullet \mathbf{nn} |^2 -
a_{sh} | (\omega_1 + \omega_2) \bullet
(\mathbf{I} - \mathbf{nn}) - 2 \Omega_N |^2 - \\
&  a_{pu} | (\omega_1 - \omega_2) \bullet (\mathbf{I} - \mathbf{nn}) |^2 -
a_{tw} | (\omega_1 - \omega_2) \bullet \mathbf{nn} |^2  \qquad r < r_c \\
& \\
\Omega_N & = \mathbf{n} \times (v_1 - v_2) / r\end{split}\]

which represents the dissipation W between two nearby particles due to
their relative velocities in the presence of a background solvent with
viscosity mu.  Note that this is dynamic viscosity which has units of
mass/distance/time, not kinematic viscosity.

The Asq (squeeze) term is the strongest and is included if flagHI is
set to 1 (default). It scales as 1/gap where gap is the separation
between the surfaces of the 2 particles. The Ash (shear) and Apu
(pump) terms are only included if flaglog is set to 1. They are the
next strongest interactions, and the only other singular interaction,
and scale as log(gap). Note that flaglog = 1 and flagHI = 0 is
invalid, and will result in a warning message, after which flagHI will
be set to 1. The Atw (twist) term is currently not included. It is
typically a very small contribution to the lubrication forces.

The flagHI and flagVF settings are optional.  Neither should be
used, or both must be defined.

Cutinner sets the minimum center-to-center separation that will be
used in calculations irrespective of the actual separation.  Cutoff
is the maximum center-to-center separation at which an interaction is
computed.  Using a cutoff less than 3 radii is recommended if
flaglog is set to 1.

The other component is due to the Fast Lubrication Dynamics (FLD)
approximation, described in (Kumar), which can be
represented by the following equation

\[F^{H} = -R_{FU}(U-U^{\infty}) + R_{FE}E^{\infty}\]

where U represents the velocities and angular velocities of the
particles, \(U^{\infty}\) represents the velocity and the angular velocity
of the undisturbed fluid, and \(E^{\infty}\) represents the rate of strain
tensor of the undisturbed fluid with viscosity mu. Again, note that
this is dynamic viscosity which has units of mass/distance/time, not
kinematic viscosity. Volume fraction corrections to R_FU are included
as long as flagVF is set to 1 (default).

Note
When using the FLD terms, these pair styles are designed to be used
with explicit time integration and a correspondingly small timestep.
Thus either fix nve/sphere or fix
nve/asphere should be used for time integration.
To perform implicit FLD, see the pair_style lubricateU command.

Style lubricate requires monodisperse spherical particles; style
lubricate/poly allows for polydisperse spherical particles.

Changed in version 4Jul2026.

The near-field resistance functions used by lubricate/poly for
particles of unequal radii were corrected so that the pairwise
lubrication force obeys Newton s third law (is equal and opposite).
Previously the log-order terms were evaluated using a per-particle
reference length, which made the force on particle i differ from
minus the force on particle j for strongly polydisperse pairs.
Results for monodisperse systems are unchanged.

The viscosity mu can be varied in a time-dependent manner over the
course of a simulation, in which case in which case the pair_style
setting for mu will be overridden.  See the fix adapt
command for details.

If the suspension is sheared via the fix deform
command then the pair style uses the shear rate to adjust the
hydrodynamic interactions accordingly. Volume changes due to fix
deform are accounted for when computing the volume fraction
corrections to R_FU.

When computing the volume fraction corrections to R_FU, the presence of
walls (whether moving or stationary) will affect the volume fraction
available to colloidal particles. This is currently accounted for with
the following types of walls: wall/lj93,
wall/lj126, wall/colloid, and
wall/harmonic.  For these wall styles, the correct
volume fraction will be used when walls do not coincide with the box
boundary, as well as when walls move and thereby cause a change in the
volume fraction.  Other wall styles may still work, but they will result
in the volume fraction being computed based on the box boundaries.
Several wall styles are not compatible with these pair styles and using
them will result in an error.

Since lubrication forces are dissipative, it is usually desirable to
thermostat the system at a constant temperature. If Brownian motion
(at a constant temperature) is desired, it can be set using the
pair_style brownian command. These pair styles
and the brownian style should use consistent parameters for mu,
flaglog, flagfld, cutinner, cutoff, flagHI and flagVF.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The two coefficients are optional.  If neither is specified, the two
cutoffs specified in the pair_style command are used.  Otherwise both
must be specified.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lubricate 1.5 1 1 2.01 2.5
pair_coeff 1 1 2.05 2.8
pair_coeff * *

pair_style lubricate 1.5 1 1 2.01 2.5
pair_coeff * *
variable mu equal ramp(1,2)
fix 1 all adapt 1 pair lubricate mu * * v_mu
```

## Restrictions

Restrictions 
These styles are part of the COLLOID package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
Only spherical monodisperse particles are allowed for pair_style
lubricate.
Only spherical particles are allowed for pair_style lubricate/poly.
These pair styles will not restart exactly when using the
read_restart command, though they should provide
statistically similar results.  This is because the forces they
compute depend on atom velocities.  See the
read_restart command for more details.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lubricateU](pair_lubricateU.html)

