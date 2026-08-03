---
id: compute_smd_tlsph_dt
title: "compute smd/tlsph/dt command"
url: https://docs.lammps.org/compute_smd_tlsph_dt.html
---

# compute smd/tlsph/dt command

## Syntax

```
compute ID group-ID smd/tlsph/dt
```

## Description

Define a computation that outputs the CFL-stable time increment per
particle.  This time increment is essentially given by the speed of
sound, divided by the SPH smoothing length.  Because both the speed of
sound and the smoothing length typically change during the course of a
simulation, the stable time increment needs to be re-computed every
time step.  This calculation is performed automatically in the
relevant SPH pair styles and this compute only serves to make the
stable time increment accessible for output purposes.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/tlsph/dt
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This compute can only be used for particles interacting with the
Total-Lagrangian SPH pair style.

## Related Commands

- [smd/adjust/dt](fix_smd_adjust_dt.html)

