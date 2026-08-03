---
id: compute_smd_tlsph_stress
title: "compute smd/tlsph/stress command"
url: https://docs.lammps.org/compute_smd_tlsph_stress.html
---

# compute smd/tlsph/stress command

## Syntax

```
compute ID group-ID smd/tlsph/stress
```

## Description

Define a computation that outputs the Cauchy stress tensor for
particles interacting via the Total-Lagrangian SPH pair style.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/tlsph/stress
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This quantity will be computed only for particles which interact with
the Total-Lagrangian SPH pair style.

## Related Commands

- [compute smd/tlsph/strain](compute_smd_tlsph_strain.html)
- [cmopute smd/tlsph/strain/rate](compute_smd_tlsph_strain_rate.html)

