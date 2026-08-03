---
id: compute_smd_rho
title: "compute smd/rho command"
url: https://docs.lammps.org/compute_smd_rho.html
---

# compute smd/rho command

## Syntax

```
compute ID group-ID smd/rho
```

## Description

Define a computation that calculates the per-particle mass density.
The mass density is the mass of a particle which is constant during
the course of a simulation, divided by its volume, which can change
due to mechanical deformation.

See this PDF guide to use Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/rho
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [compute smd/vol](compute_smd_vol.html)

