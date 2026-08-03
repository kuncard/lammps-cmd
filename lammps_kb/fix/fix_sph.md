---
id: fix_sph
title: "fix sph command"
url: https://docs.lammps.org/fix_sph.html
---

# fix sph command

## Syntax

```
fix ID group-ID sph
```

## Description

Perform time integration to update position, velocity, internal energy
and local density for atoms in the group each timestep. This fix is
needed to time-integrate SPH systems where particles carry internal
variables such as internal energy.  SPH stands for Smoothed Particle
Hydrodynamics.

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
fix 1 all sph
```

## Restrictions

Restrictions 
This fix is part of the SPH package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix sph/stationary](fix_sph_stationary.html)

