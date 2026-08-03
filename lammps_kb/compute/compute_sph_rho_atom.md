---
id: compute_sph_rho_atom
title: "compute sph/rho/atom command"
url: https://docs.lammps.org/compute_sph_rho_atom.html
---

# compute sph/rho/atom command

## Syntax

```
compute ID group-ID sph/rho/atom
```

## Description

Define a computation that calculates the per-atom SPH density for each
atom in a group, i.e. a Smooth-Particle Hydrodynamics density.

The SPH density is the mass density of an SPH particle, calculated by
kernel function interpolation using  pair style sph/rhosum .

See this PDF guide to using SPH in
LAMMPS.

Note
Please note that the SPH PDF guide file has not been updated for
many years and thus does not reflect the current syntax of the
SPH package commands. For that please refer to the LAMMPS manual.

The value of the SPH density will be 0.0 for atoms not in the
specified compute group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all sph/rho/atom
```

## Restrictions

Restrictions 
This compute is part of the SPH package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [dump custom](dump.html)

