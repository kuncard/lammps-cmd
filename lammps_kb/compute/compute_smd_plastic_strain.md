---
id: compute_smd_plastic_strain
title: "compute smd/plastic/strain command"
url: https://docs.lammps.org/compute_smd_plastic_strain.html
---

# compute smd/plastic/strain command

## Syntax

```
compute ID group-ID smd/plastic/strain
```

## Description

Define a computation that outputs the equivalent plastic strain per
particle.  This command is only meaningful if a material model with
plasticity is defined.

See this PDF guide to use Smooth
Mach Dynamics in LAMMPS.

Output Info:

This compute calculates a per-particle vector, which can be accessed
by any command that uses per-particle values from a compute as input.
See the Howto output page for an overview of
LAMMPS output options.

The per-particle values will be given dimensionless. See units.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/plastic/strain
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info. This compute can
only be used for particles which interact via the updated Lagrangian
or total Lagrangian SPH pair styles.

## Related Commands

- [smd/plastic/strain/rate](compute_smd_tlsph_strain.html)
- [smd/tlsph/strain/rate](compute_smd_tlsph_strain_rate.html)
- [smd/tlsph/strain](compute_smd_tlsph_strain.html)

