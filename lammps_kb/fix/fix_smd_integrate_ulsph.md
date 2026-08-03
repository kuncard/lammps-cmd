---
id: fix_smd_integrate_ulsph
title: "fix smd/integrate_ulsph command"
url: https://docs.lammps.org/fix_smd_integrate_ulsph.html
---

# fix smd/integrate_ulsph command

## Syntax

```
fix ID group-ID smd/integrate_ulsph keyword
```

## Description

The fix performs explicit time integration for particles which
interact with the updated Lagrangian SPH pair style.

See this PDF guide to using Smooth Mach
Dynamics in LAMMPS.

The adjust_radius keyword activates dynamic adjustment of the
per-particle SPH smoothing kernel radius such that the number of
neighbors per particles remains within the interval min_nn to
max_nn. The parameter adjust_radius_factor determines the amount
of adjustment per timestep. Typical values are adjust_radius_factor
=1.02, min_nn =15, and max_nn =20.

The limit_velocity keyword will control the velocity, scaling the norm of
the velocity vector to max_vel in case it exceeds this velocity limit.

## Keywords

- **adjust_radius values = adjust_radius_factor min_nn max_nn**: adjust_radius_factor = factor which scale the smooth/kernel radius
min_nn = minimum number of neighbors
max_nn = maximum number of neighbors
- **limit_velocity values = max_velocity**: max_velocity = maximum allowed velocity.
- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all smd/integrate_ulsph adjust_radius 1.02 25 50
fix 1 all smd/integrate_ulsph limit_velocity 1000
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

Changed in version 29Aug2024.

This fix is incompatible with deformation controls that remap velocity,
for instance the remap v option of fix deform.

## Related Commands

Related commands 
none

