---
id: pair_surf_granular
title: "pair_style surf/granular command"
url: https://docs.lammps.org/pair_surf_granular.html
---

# pair_style surf/granular command

## Syntax

```
pair_style surf/granular cutoff
```

## Description

Added in version 4Jul2026.

The surf/granular pair style is designed for interactions between
granular surfaces made out of lines/triangles and finite-sized atoms
and must be used in conjunction with fix surface/local.  See the Howto granular surfaces doc page for more information on granular
surfaces.

The equation for the force between a triangle/line and a particle
touching it is the same as the corresponding equation on the
pair_style granular doc page in the limit of
one of the two particles going to infinite radius and mass (flat
surface).  Specifically, \(\delta\) = overlap of particle with
triangle/line, \(m_eff\) = mass of particle, and the effective
radius of contact R_{eff}= R_i R_j/R_i + R_j is set to the radius of
the particle. See the Howto granular surfaces doc page for information on how overlaps
and normal vectors are calculated based on the geometry of the surface
and when friction is transferred between lines/triangles.

All model choices and parameters are entered in the pair_coeff command.  Coefficient values are not global, but can be
set to different values for different combinations of particle types,
as determined by the pair_coeff command.  If the
contact model choice is the same for two particle types, the mixing
for the cross-coefficients can be carried out automatically.  For
additional flexibility, coefficients as well as model forms can vary
between particle types. Available pair coefficients and contact models
are identical to those in the granular pair
style. The only exception is that forces cannot extend beyond contact
as in the JKR contact model.

LAMMPS automatically sets pairwise cutoff values for pair_style
granular based on the atom radii.  In the vast majority of situations,
this is adequate. However, a cutoff value can optionally be appended to
the pair_style granular command to specify a global cutoff (i.e. a
cutoff for all atom types).  Additionally, the optional cutoff keyword
can be passed to the pair_coeff command, followed by a cutoff value.
This will set a pairwise cutoff for the atom types in the pair_coeff
command.  These options may be useful in some rare cases where the automatic
cutoff determination is not sufficient, e.g.  if particle diameters are
being modified via the fix adapt command.  In that case, the global cutoff
specified as part of the pair_style granular command is applied to all
atom types, unless it is overridden for a given atom type combination by
the cutoff value specified in the pair coeff command.  If cutoff
is only specified in the pair coeff command and no global cutoff is
appended to the pair_style granular command, then LAMMPS will use that
cutoff for the specified atom type combination, and automatically set
pairwise cutoffs for the remaining atom types.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style surf/granular
pair_coeff * * hooke 1000.0 50.0 tangential linear_nohistory 1.0 0.4 damping mass_velocity

pair_style surf/granular
pair_coeff * * hooke 1000.0 50.0 tangential linear_history 500.0 1.0 0.4 damping mass_velocity
```

## Restrictions

Restrictions 
This pair style is part of the GRANSURF package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
This pair style must be in used in conjunction with
fix surface/local.
This pair style requires the data structures in atom_style line in 2d and atom_style line in 3d.
Additionally, this pair style requires that atoms store per-particle radius,
torque, and angular velocity (omega). These quantities are defined by
the line/tri atom styles, however, the radii are not written to data
files so it is recommended to hybridize these atom styles with
atom style sphere using atom style hybrid.
This pair style requires you to use the comm_modify vel yes
command so that velocities are stored by ghost atoms.
This pair style will not restart exactly when using the
read_restart command, though it should provide
statistically similar results.  This is because the forces it
computes depend on atom velocities and the atom velocities have
been propagated half a timestep between the force computation and
when the restart is written, due to using Velocity Verlet time
integration. See the read_restart command
for more details.
Accumulated values for individual contacts are saved to restart
files but are not saved to data files. Therefore, forces may
differ significantly when a system is reloaded using the
read_data command.

## Related Commands

- [fix surface/local](fix_surface_local.html)
- [fix pair/granular](pair_granular.html)

