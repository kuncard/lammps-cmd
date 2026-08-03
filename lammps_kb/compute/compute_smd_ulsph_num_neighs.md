---
id: compute_smd_ulsph_num_neighs
title: "compute smd/ulsph/num/neighs command"
url: https://docs.lammps.org/compute_smd_ulsph_num_neighs.html
---

# compute smd/ulsph/num/neighs command

## Syntax

```
compute ID group-ID smd/ulsph/num/neighs
```

## Description

Define a computation that returns the number of neighbor particles
inside of the smoothing kernel radius for particles interacting via
the updated Lagrangian SPH pair style.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/ulsph/num/neighs
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.  This compute can
only be used for particles which interact with the updated Lagrangian
SPH pair style.

## Related Commands

- [compute smd/tlsph/num/neighs](compute_smd_tlsph_num_neighs.html)

