---
id: compute_smd_tlsph_num_neighs
title: "compute smd/tlsph/num/neighs command"
url: https://docs.lammps.org/compute_smd_tlsph_num_neighs.html
---

# compute smd/tlsph/num/neighs command

## Syntax

```
compute ID group-ID smd/tlsph/num/neighs
```

## Description

Define a computation that calculates the number of particles inside of
the smoothing kernel radius for particles interacting via the
Total-Lagrangian SPH pair style.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/tlsph/num/neighs
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This quantity will be computed only for particles which interact with
the Total-Lagrangian pair style.

## Related Commands

- [smd/ulsph/num/neighs](compute_smd_ulsph_num_neighs.html)

