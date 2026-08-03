---
id: fix_nve_asphere_noforce
title: "fix nve/asphere/noforce command"
url: https://docs.lammps.org/fix_nve_asphere_noforce.html
---

# fix nve/asphere/noforce command

## Syntax

```
fix ID group-ID nve/asphere/noforce
```

## Description

Perform updates of position and orientation, but not velocity or
angular momentum for atoms in the group each timestep.  In other
words, the force and torque on the atoms is ignored and their velocity
and angular momentum are not updated.  The atom velocities and
angular momenta are used to update their positions and orientation.

This is useful as an implicit time integrator for Fast Lubrication
Dynamics, since the velocity and angular momentum are updated by the
pair_style lubricuteU command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/asphere/noforce
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

- [fix nve/noforce](fix_nve_noforce.html)
- [fix nve/asphere](fix_nve_asphere.html)

