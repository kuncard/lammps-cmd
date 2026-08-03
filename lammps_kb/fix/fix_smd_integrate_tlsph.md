---
id: fix_smd_integrate_tlsph
title: "fix smd/integrate_tlsph command"
url: https://docs.lammps.org/fix_smd_integrate_tlsph.html
---

# fix smd/integrate_tlsph command

## Syntax

```
fix ID group-ID smd/integrate_tlsph keyword values
limit_velocity value = max_vel
  max_vel = maximum allowed velocity
```

## Description

The fix performs explicit time integration for particles which
interact according with the Total-Lagrangian SPH pair style.

See this PDF guide to using Smooth Mach
Dynamics in LAMMPS.

The limit_velocity keyword will control the velocity, scaling the
norm of the velocity vector to max_vel in case it exceeds this
velocity limit.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all smd/integrate_tlsph
fix 1 all smd/integrate_tlsph limit_velocity 1000
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

Changed in version 29Aug2024.

This fix is incompatible with deformation controls that remap velocity,
for instance the remap v option of fix deform.

## Related Commands

- [smd/integrate_ulsph](fix_smd_integrate_ulsph.html)

