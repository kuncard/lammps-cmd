---
id: pair_tri_lj
title: "pair_style tri/lj command"
url: https://docs.lammps.org/pair_tri_lj.html
---

# pair_style tri/lj command

## Syntax

```
pair_style tri/lj cutoff
```

## Description

Style tri/lj treats particles which are triangles as a set of small
spherical particles that tile the triangle surface as explained below.
Interactions between two triangles, each with N1 and N2 spherical
particles, are calculated as the pairwise sum of N1*N2 Lennard-Jones
interactions.  Interactions between a triangle with N spherical
particles and a point particle are treated as the pairwise sum of N
Lennard-Jones interactions.  See the pair_style lj/cut
doc page for the definition of Lennard-Jones interactions.

The cutoff distance for an interaction between 2 triangles, or between
a triangle and a point particle, is calculated from the position of
the triangle (its centroid), not between pairs of individual spheres
comprising the triangle.  Thus an interaction is either calculated in
its entirety or not at all.

The set of non-overlapping spherical particles that represent a
triangle, for purposes of this pair style, are generated in the
following manner.  Assume the triangle is of type I, and sigma_II has
been specified.  We want a set of spheres with centers in the plane of
the triangle, none of them larger in diameter than sigma_II, which
completely cover the triangle s area, but with minimal overlap and a
minimal total number of spheres.  This is done in a recursive manner.
Place a sphere at the centroid of the original triangle.  Calculate
what diameter it must have to just cover all 3 corner points of the
triangle.  If that diameter is equal to or smaller than sigma_II, then
include a sphere of the calculated diameter in the set of covering
spheres.  It the diameter is larger than sigma_II, then split the
triangle into 2 triangles by bisecting its longest side.  Repeat the
process on each sub-triangle, recursing as far as needed to generate a
set of covering spheres.  When finished, the original criteria are
met, and the set of covering spheres should be near minimal in number
and overlap, at least for input triangles with a reasonable
aspect-ratio.

The LJ interaction between 2 spheres on different triangles of types
I,J is computed with an arithmetic mixing of the sigma values of the 2
spheres and using the specified epsilon value for I,J atom types.
Note that because the sigma values for triangles spheres is computed
using only sigma_II values, specific to the triangles s type, this
means that any specified sigma_IJ values (for I != J) are effectively
ignored.

For style tri/lj, the following coefficients must be defined for
each pair of atoms types via the pair_coeff command
as in the examples above, or in the data file or restart files read by
the read_data or read_restart
commands:

The last coefficient is optional.  If not specified, the global cutoff
is used.

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
pair_style tri/lj 3.0
pair_coeff * * 1.0 1.0
pair_coeff 1 1 1.0 1.5 2.5
```

## Restrictions

Restrictions 
This style is part of the ASPHERE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Defining particles to be triangles so they participate in tri/tri or
tri/particle interactions requires the use the atom_style tri command.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style line/lj](pair_line_lj.html)

