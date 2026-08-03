---
id: fix_nve_tri
title: "fix nve/tri command"
url: https://docs.lammps.org/fix_nve_tri.html
---

# fix nve/tri command

## Syntax

```
fix ID group-ID nve/tri
```

## Description

Perform constant NVE integration to update position, velocity,
orientation, and angular momentum for triangular particles in the
group each timestep.  V is volume; E is energy.  This creates a system
trajectory consistent with the microcanonical ensemble.  See the
Howto spherical page for an overview of
using triangular particles.

This fix differs from the fix nve command, which
assumes point particles and only updates their position and velocity.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/tri
```

## Restrictions

Restrictions 
This fix is part of the ASPHERE package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that particles be triangles as defined by the
atom_style tri command.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nve/asphere](fix_nve_asphere.html)

