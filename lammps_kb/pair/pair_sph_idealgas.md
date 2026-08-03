---
id: pair_sph_idealgas
title: "pair_style sph/idealgas command"
url: https://docs.lammps.org/pair_sph_idealgas.html
---

# pair_style sph/idealgas command

## Syntax

```
pair_style sph/idealgas
```

## Description

The sph/idealgas style computes pressure forces between particles
according to the ideal gas equation of state:

\[p = (\gamma - 1) \rho e\]

where \(\gamma = 1.4\) is the heat capacity ratio, \(\rho\) is
the local density, and e is the internal energy per unit mass.  This
pair style also computes Monaghan s artificial viscosity to prevent
particles from interpenetrating (Monaghan).

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
pair_style sph/idealgas
pair_coeff * * 1.0 2.4
```

## Restrictions

Restrictions 
This pair style is part of the SPH package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

