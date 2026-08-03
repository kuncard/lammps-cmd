---
id: compute_smd_hourglass_error
title: "compute smd/hourglass/error command"
url: https://docs.lammps.org/compute_smd_hourglass_error.html
---

# compute smd/hourglass/error command

## Syntax

```
compute ID group-ID smd/hourglass/error
```

## Description

Define a computation which outputs the error of the approximated
relative separation with respect to the actual relative separation of
the particles i and j. Ideally, if the deformation gradient is exact,
and there exists a unique mapping between all particles  positions
within the neighborhood of the central node and the deformation
gradient, the approximated relative separation will coincide with the
actual relative separation of the particles i and j in the deformed
configuration.  This compute is only really useful for debugging the
hourglass control mechanism which is part of the Total-Lagrangian SPH
pair style.

See this PDF guide to use Smooth
Mach Dynamics in LAMMPS.

Output Info:

This compute calculates a per-particle vector, which can be accessed
by any command that uses per-particle values from a compute as input.
See the Howto output page for an overview of
LAMMPS output options.

The per-particle vector values will are dimensionless. See
units.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/hourglass/error
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This quantity will be computed only for particles which interact with
tlsph pair style.

## Related Commands

- [smd/tlsph_defgrad](compute_smd_tlsph_defgrad.html)

