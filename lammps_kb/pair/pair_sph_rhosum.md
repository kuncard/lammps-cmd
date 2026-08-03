---
id: pair_sph_rhosum
title: "pair_style sph/rhosum command"
url: https://docs.lammps.org/pair_sph_rhosum.html
---

# pair_style sph/rhosum command

## Syntax

```
pair_style sph/rhosum Nstep
```

## Description

The sph/rhosum style computes the local particle mass density rho for
SPH particles by kernel function interpolation, every Nstep timesteps.

See this PDF guide to using SPH in
LAMMPS.

Note
Please note that the SPH PDF guide file has not been updated for
many years and thus does not reflect the current syntax of the
SPH package commands. For that please refer to the LAMMPS manual.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style sph/rhosum 10
pair_coeff * * 2.4
```

## Restrictions

Restrictions 
This pair style is part of the SPH package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

