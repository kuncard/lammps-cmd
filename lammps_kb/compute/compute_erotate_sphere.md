---
id: compute_erotate_sphere
title: "compute erotate/sphere command"
url: https://docs.lammps.org/compute_erotate_sphere.html
---

# compute erotate/sphere command

## Syntax

```
compute ID group-ID erotate/sphere
```

## Description

Define a computation that calculates the rotational kinetic energy of
a group of spherical particles.

The rotational energy is computed as \(\frac12 I \omega^2\),
where \(I\) is the moment of inertia for a sphere and \(\omega\)
is the particle s angular velocity.

Note
For 2d models, particles are treated as
spheres, not disks, meaning their moment of inertia will be the same
as in 3d.

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
compute 1 all erotate/sphere
```

## Restrictions

Restrictions 
This compute requires that atoms store a radius and angular velocity
(omega) as defined by the atom_style sphere command.
All particles in the group must be finite-size spheres or point
particles.  They cannot be aspherical.  Point particles will not
contribute to the rotational energy.

## Related Commands

- [compute erotate/asphere](compute_erotate_asphere.html)

