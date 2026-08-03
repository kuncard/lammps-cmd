---
id: fix_nvk
title: "fix nvk command"
url: https://docs.lammps.org/fix_nvk.html
---

# fix nvk command

## Syntax

```
fix ID group-ID nvk
```

## Description

Perform constant kinetic energy integration using the Gaussian
thermostat to update position and velocity for atoms in the group each
timestep.  V is volume; K is kinetic energy. This creates a system
trajectory consistent with the isokinetic ensemble.

The equations of motion used are those of Minary et al in
(Minary), a variant of those initially given by Zhang in
(Zhang).

The kinetic energy will be held constant at its value given when fix
nvk is initiated. If a different kinetic energy is desired, the
velocity command should be used to change the kinetic
energy prior to this fix.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nvk
```

## Restrictions

Restrictions 
The Gaussian thermostat only works when it is applied to all atoms in
the simulation box. Therefore, the group must be set to all.
This fix has not yet been implemented to work with the RESPA integrator.
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

Related commands 
none

