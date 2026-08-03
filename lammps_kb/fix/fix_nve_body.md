---
id: fix_nve_body
title: "fix nve/body command"
url: https://docs.lammps.org/fix_nve_body.html
---

# fix nve/body command

## Syntax

```
fix ID group-ID nve/body
```

## Description

Perform constant NVE integration to update position, velocity,
orientation, and angular velocity for body particles in the group each
timestep.  V is volume; E is energy.  This creates a system trajectory
consistent with the microcanonical ensemble.  See the Howto body page for more details on using body
particles.

This fix differs from the fix nve command, which
assumes point particles and only updates their position and velocity.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/body
```

## Restrictions

Restrictions 
This fix is part of the BODY package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that atoms store torque and angular momentum and a
quaternion as defined by the atom_style body
command.
All particles in the group must be body particles.  They cannot be
point particles.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nve/sphere](fix_nve_sphere.html)
- [fix nve/asphere](fix_nve_asphere.html)

