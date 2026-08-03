---
id: fix_nve_line
title: "fix nve/line command"
url: https://docs.lammps.org/fix_nve_line.html
---

# fix nve/line command

## Syntax

```
fix ID group-ID nve/line
```

## Description

Perform constant NVE integration to update position, velocity,
orientation, and angular velocity for line segment particles in the
group each timestep.  V is volume; E is energy.  This creates a system
trajectory consistent with the microcanonical ensemble.  See Howto spherical page for an overview of using line
segment particles.

This fix differs from the fix nve command, which
assumes point particles and only updates their position and velocity.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/line
```

## Restrictions

Restrictions 
This fix is part of the ASPHERE package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that particles be line segments as defined by the
atom_style line command.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nve/asphere](fix_nve_asphere.html)

