---
id: compute_smd_internal_energy
title: "compute smd/internal/energy command"
url: https://docs.lammps.org/compute_smd_internal_energy.html
---

# compute smd/internal/energy command

## Syntax

```
compute ID group-ID smd/internal/energy
```

## Description

Define a computation which outputs the per-particle enthalpy, i.e.,
the sum of potential energy and heat.

See this PDF guide to use Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/internal/energy
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info. This compute can
only be used for particles which interact via the updated Lagrangian
or total Lagrangian SPH pair styles.

## Related Commands

Related commands 
none

