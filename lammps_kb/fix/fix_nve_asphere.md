---
id: fix_nve_asphere
title: "fix nve/asphere command"
url: https://docs.lammps.org/fix_nve_asphere.html
---

# fix nve/asphere command

## Syntax

```
fix ID group-ID nve/asphere
```

## Description

Perform constant NVE integration to update position, velocity,
orientation, and angular velocity for aspherical particles in the
group each timestep.  V is volume; E is energy.  This creates a system
trajectory consistent with the microcanonical ensemble.

This fix differs from the fix nve command, which
assumes point particles and only updates their position and velocity.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/asphere
```

## Restrictions

Restrictions 
This fix is part of the ASPHERE package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that atoms store torque and angular momentum and a
quaternion as defined by the atom_style ellipsoid
command.
All particles in the group must be finite-size.  They cannot be point
particles, but they can be aspherical or spherical as defined by their
shape attribute.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nve/sphere](fix_nve_sphere.html)

