---
id: fix_viscous_sphere
title: "fix viscous/sphere command"
url: https://docs.lammps.org/fix_viscous_sphere.html
---

# fix viscous/sphere command

## Syntax

```
fix ID group-ID viscous/sphere gamma keyword values ...
keyword = scale
  scale values = type ratio or v_name
    type = atom type (1-N)
    ratio = factor to scale the damping coefficients by
    v_name = reference to atom style variable name
```

## Description

Add a viscous damping torque to finite-size spherical particles in the group
that is proportional to the angular velocity of the atom.  In granular
simulations this can be useful for draining the rotational kinetic energy from
the system in a controlled fashion.  If used without additional thermostatting
(to add kinetic energy to the system), it has the effect of slowly (or rapidly)
freezing the system; hence it can also be used as a simple energy minimization
technique.

The damping torque \(T_i\) is given by \(T_i = - \gamma \omega_i\).
The larger the coefficient, the faster the rotational kinetic energy is reduced.

If the optional keyword scale is used, \(\gamma\) can be scaled up
or down by the specified factor for atoms.  This factor can be set for
different atom types and thus the scale keyword used multiple times
followed by the atom type and the associated scale factor.  Alternately
the scaling factor can be computed for each atom (e.g. based on its
radius) by using an atom-style variable.

Note
You should specify gamma in torque/angular velocity units.  This is not
the same as mass/time units, at least for some of the LAMMPS
units options like  real  or  metal  that are not
self-consistent.

In the current implementation, rather than have the user specify a viscosity,
\(\gamma\) is specified directly in torque/angular velocity units.
If needed, \(\gamma\) can be adjusted for atoms of different sizes
(i.e. \(\sigma\)) by using the scale keyword.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 flow viscous/sphere 0.1
fix 1 damp viscous/sphere 0.5 scale 3 2.5
fix 1 damp viscous/sphere 0.5 scale v_radscale
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This fix requires that atoms store torque and angular velocity (omega)
and a radius as defined by the atom_style sphere
command.
All particles in the group must be finite-size spheres.  They cannot
be point particles.

## Related Commands

- [fix viscous](fix_viscous.html)
- [fix damping/cundall](fix_damping_cundall.html)

