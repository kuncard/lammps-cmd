---
id: compute_smd_vol
title: "compute smd/vol command"
url: https://docs.lammps.org/compute_smd_vol.html
---

# compute smd/vol command

## Syntax

```
compute ID group-ID smd/vol
```

## Description

Define a computation that provides the per-particle volume and the sum
of the per-particle volumes of the group for which the compute is defined.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/vol
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [compute smd/rho](compute_smd_rho.html)

