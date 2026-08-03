---
id: compute_smd_ulsph_effm
title: "compute smd/ulsph/effm command"
url: https://docs.lammps.org/compute_smd_ulsph_effm.html
---

# compute smd/ulsph/effm command

## Syntax

```
compute ID group-ID smd/ulsph/effm
```

## Description

Define a computation that outputs the effective shear modulus for
particles interacting via the updated Lagrangian SPH pair style.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/ulsph/effm
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info. This compute can
only be used for particles which interact with the updated Lagrangian
SPH pair style.

## Related Commands

- [pair smd/ulsph](pair_smd_ulsph.html)

