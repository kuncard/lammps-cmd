---
id: compute_smd_ulsph_strain_rate
title: "compute smd/ulsph/strain/rate command"
url: https://docs.lammps.org/compute_smd_ulsph_strain_rate.html
---

# compute smd/ulsph/strain/rate command

## Syntax

```
compute ID group-ID smd/ulsph/strain/rate
```

## Description

Define a computation that outputs the rate of the logarithmic strain
tensor for particles interacting via the updated Lagrangian SPH pair
style.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/ulsph/strain/rate
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This compute can only be used for particles which interact with the
updated Lagrangian SPH pair style.

## Related Commands

- [compute smd/tlsph/strain/rate](compute_smd_tlsph_strain_rate.html)

