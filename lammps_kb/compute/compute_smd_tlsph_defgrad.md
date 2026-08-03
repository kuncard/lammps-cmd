---
id: compute_smd_tlsph_defgrad
title: "compute smd/tlsph/defgrad command"
url: https://docs.lammps.org/compute_smd_tlsph_defgrad.html
---

# compute smd/tlsph/defgrad command

## Syntax

```
compute ID group-ID smd/tlsph/defgrad
```

## Description

Define a computation that calculates the deformation gradient.  It is
only meaningful for particles which interact according to the
Total-Lagrangian SPH pair style.

See this PDF guide to use Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/tlsph/defgrad
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info. TThis compute can
only be used for particles which interact via the total Lagrangian SPH
pair style.

## Related Commands

- [smd/hourglass/error](compute_smd_hourglass_error.html)

