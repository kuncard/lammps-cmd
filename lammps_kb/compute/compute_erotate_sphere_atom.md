---
id: compute_erotate_sphere_atom
title: "compute erotate/sphere/atom command"
url: https://docs.lammps.org/compute_erotate_sphere_atom.html
---

# compute erotate/sphere/atom command

## Syntax

```
compute ID group-ID erotate/sphere/atom
```

## Description

Define a computation that calculates the rotational kinetic energy for
each particle in a group.

The rotational energy is computed as \(\frac12 I \omega^2\), where
\(I\) is the moment of inertia for a sphere and \(\omega\) is the
particle s angular velocity.

Note
For 2d models, particles are treated as
spheres, not disks, meaning their moment of inertia will be the same
as in 3d.

The value of the rotational kinetic energy will be 0.0 for atoms not
in the specified compute group or for point particles with a radius of 0.0.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all erotate/sphere/atom
```

## Restrictions

Restrictions 
none

## Related Commands

- [dump custom](dump.html)

