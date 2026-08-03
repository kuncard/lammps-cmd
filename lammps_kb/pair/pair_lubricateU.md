---
id: pair_lubricateU
title: "pair_style lubricateU command"
url: https://docs.lammps.org/pair_lubricateU.html
---

# pair_style lubricateU command

## Syntax

```
pair_style style mu flaglog cutinner cutoff gdot flagHI flagVF
```

## Description

Styles lubricateU and lubricateU/poly compute velocities and
angular velocities for finite-size spherical particles such that the
hydrodynamic interaction balances the force and torque due to all
other types of interactions.

The interactions have 2 components.  The first is
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

The Asq (squeeze) term is the strongest and is included as long as
flagHI is set to 1 (default). It scales as 1/gap where gap is the
separation between the surfaces of the 2 particles. The Ash (shear)
and Apu (pump) terms are only included if flaglog is set to 1. They
are the next strongest interactions, and the only other singular
interaction, and scale as log(gap). Note that flaglog = 1 and
flagHI = 0 is invalid, and will result in a warning message, after
which flagHI will be set to 1. The Atw (twist) term is currently not
included. It is typically a very small contribution to the lubrication
forces.

The flagHI and flagVF settings are optional.  Neither should be
used, or both must be defined.

Cutinner sets the minimum center-to-center separation that will be
used in calculations irrespective of the actual separation.  Cutoff
is the maximum center-to-center separation at which an interaction is
computed.  Using a cutoff less than 3 radii is recommended if
flaglog is set to 1.

The other component is due to the Fast Lubrication Dynamics (FLD)
approximation, described in (Kumar).  The equation being
solved to balance the forces and torques is

\[-R_{FU}(U-U^{\infty}) = -R_{FE}E^{\infty} - F^{rest}\]

where U represents the velocities and angular velocities of the
particles, \(U^{\infty}\) represents the velocities and the angular
velocities of the undisturbed fluid, and \(E^{\infty}\) represents
the rate of strain tensor of the undisturbed fluid flow with viscosity
mu. Again, note that this is dynamic viscosity which has units of
mass/distance/time, not kinematic viscosity.  Volume fraction
corrections to R_FU are included if flagVF is set to 1 (default).

Frest represents the forces and torques due to all other types of
interactions, e.g. Brownian, electrostatic etc.  Note that this
algorithm neglects the inertial terms, thereby removing the restriction
of resolving the small interial time scale, which may not be of interest
for colloidal particles.  These pair styles solve for the velocity such
that the hydrodynamic force balances all other types of forces, thereby
resulting in a net zero force (zero inertia limit).  When defining these
pair styles, they must be defined last so that when these styles are
invoked all other types of forces have already been computed.  For the
same reason, they won t work if additional non-pair styles are defined
(such as bond or Kspace forces) as they are calculated in LAMMPS after
the pairwise interactions have been computed.

Note
When using these styles, the pair styles are designed to be used with
implicit time integration and a correspondingly larger timestep.
Thus either fix nve/noforce should be used
for spherical particles defined via atom_style sphere or fix nve/asphere/noforce should be used for spherical particles
defined via atom_style ellipsoid.  This is
because the velocity and angular momentum of each particle is set by
the pair style, and should not be reset by the time integration fix.

Style lubricateU requires monodisperse spherical particles; style
lubricateU/poly allows for polydisperse spherical particles.

Changed in version 4Jul2026.

The near-field resistance functions used by lubricateU/poly for
particles of unequal radii were corrected for consistency with
pair_style lubricate/poly so that the squeeze
and shear resistances are symmetric under exchange of the two
particles.  Results for monodisperse systems are unchanged.

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
volume fraction. To use these wall styles with pair_style lubricateU
or lubricateU/poly, the fld yes option must be specified in the fix
wall command.  Other wall styles may still work, but they will result
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

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lubricateU 1.5 1 2.01 2.5 0.01 1 1
pair_coeff 1 1 2.05 2.8
pair_coeff * *
```

## Restrictions

Restrictions 
These styles are part of the COLLOID package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Currently, these pair styles assume that all other types of
forces/torques on the particles have been already been computed when it
is invoked.  This requires this style to be defined as the last of the
pair styles, and that no fixes apply additional constraint forces.  One
exception is the fix wall/colloid commands, which has
an  fld  option to apply their wall forces correctly.
Only spherical monodisperse particles are allowed for pair_style
lubricateU.
Only spherical particles are allowed for pair_style lubricateU/poly.
For sheared suspensions, it is assumed that the shearing is done in the
xy plane, with x being the velocity direction and y being the
velocity-gradient direction. In this case, one must use fix deform with the same rate of shear (erate).
These pair styles are only compatible with the following wall fixes:
doc:fix wall/lj93, fix wall/lj126, fix wall/lj1043, fix wall/colloid,
fix wall/harmonic, fix wall/lepton, fix wall/morse, fix wall/table
<fix_wall>.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lubricate](pair_lubricate.html)

