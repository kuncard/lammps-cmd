---
id: compute_smd_ulsph_stress
title: "compute smd/ulsph/stress command"
url: https://docs.lammps.org/compute_smd_ulsph_stress.html
---

# compute smd/ulsph/stress command

## Syntax

```
compute ID group-ID smd/ulsph/stress
```

## Description

Define a computation that outputs the Cauchy stress tensor.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/ulsph/stress
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info. This compute can
only be used for particles which interact with the updated Lagrangian
SPH pair style.

## Related Commands

- [compute smd/ulsph/strain](compute_smd_ulsph_strain.html)
- [compute smd/ulsph/strain/rate](compute_smd_ulsph_strain_rate.html)
- [compute smd/tlsph/stress](compute_smd_tlsph_stress.html)

