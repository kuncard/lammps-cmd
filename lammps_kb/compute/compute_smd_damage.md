---
id: compute_smd_damage
title: "compute smd/damage command"
url: https://docs.lammps.org/compute_smd_damage.html
---

# compute smd/damage command

## Syntax

```
compute ID group-ID smd/damage
```

## Description

Define a computation that calculates the damage status of SPH particles
according to the damage model which is defined via the SMD SPH pair styles, e.g., the maximum plastic strain failure criterion.

See this PDF guide to use Smooth Mach Dynamics in LAMMPS.

Output Info:

This compute calculates a per-particle vector, which can be accessed
by any command that uses per-particle values from a compute as input.
See the Howto output page for an overview of
LAMMPS output options.

The per-particle values are dimensionless an in the range of zero to one.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/damage
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the  Build

## Related Commands

- [smd/plastic_strain](compute_smd_plastic_strain.html)
- [smd/tlsph_stress](compute_smd_tlsph_stress.html)

