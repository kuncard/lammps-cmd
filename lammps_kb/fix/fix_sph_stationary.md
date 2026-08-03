---
id: fix_sph_stationary
title: "fix sph/stationary command"
url: https://docs.lammps.org/fix_sph_stationary.html
---

# fix sph/stationary command

## Syntax

```
fix ID group-ID sph/stationary
```

## Description

Perform time integration to update internal energy and local density,
but not position or velocity for atoms in the group each timestep.
This fix is needed for SPH simulations to correctly time-integrate
fixed boundary particles which constrain a fluid to a given region in
space.  SPH stands for Smoothed Particle Hydrodynamics.

See this PDF guide to using SPH in
LAMMPS.

Note
Please note that the SPH PDF guide file has not been updated for
many years and thus does not reflect the current syntax of the
SPH package commands. For that please refer to the LAMMPS manual.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 boundary sph/stationary
```

## Restrictions

Restrictions 
This fix is part of the SPH package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix sph](fix_sph.html)

