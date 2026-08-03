---
id: compute_erotate_asphere
title: "compute erotate/asphere command"
url: https://docs.lammps.org/compute_erotate_asphere.html
---

# compute erotate/asphere command

## Syntax

```
compute ID group-ID erotate/asphere
```

## Description

Define a computation that calculates the rotational kinetic energy of
a group of aspherical particles.  The aspherical particles can be
ellipsoids, or line segments, or triangles.  See the
atom_style and read_data commands
for descriptions of these options.

For all 3 types of particles, the rotational kinetic energy is
computed as \(\frac12 I \omega^2\), where \(I\) is the inertia tensor
for the aspherical particle and \(\omega\) is its angular velocity, which
is computed from its angular momentum if needed.

Note
For 2d models, ellipsoidal particles are
treated as ellipsoids, not ellipses, meaning their moments of inertia
will be the same as in 3d.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all erotate/asphere
```

## Restrictions

Restrictions 
This compute requires that ellipsoidal particles atoms store a shape
and quaternion orientation and angular momentum as defined by the
atom_style ellipsoid command.
This compute requires that line segment particles atoms store a length
and orientation and angular velocity as defined by the atom_style line command.
This compute requires that triangular particles atoms store a size and
shape and quaternion orientation and angular momentum as defined by
the atom_style tri command.
All particles in the group must be of finite size.  They cannot be point
particles.

## Related Commands

- [compute erotate/sphere](compute_erotate_sphere.html)

