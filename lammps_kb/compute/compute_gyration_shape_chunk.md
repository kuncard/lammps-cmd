---
id: compute_gyration_shape_chunk
title: "compute gyration/shape/chunk command"
url: https://docs.lammps.org/compute_gyration_shape_chunk.html
---

# compute gyration/shape/chunk command

## Syntax

```
compute ID group-ID gyration/shape/chunk compute-ID
```

## Description

Define a computation that calculates the eigenvalues of the gyration tensor and
three shape parameters of multiple chunks of atoms. The computation includes
all effects due to atoms passing through periodic boundaries.

The three computed shape parameters are the asphericity, \(b\),
the acylindricity, \(c\), and the relative shape anisotropy, \(k\),
viz.,

\[\begin{split}b &= l_z - \frac12(l_y+l_x) \\
c &= l_y - l_x \\
k &= \frac{3}{2} \frac{l_x^2+l_y^2+l_z^2}{(l_x+l_y+l_z)^2} - \frac{1}{2}\end{split}\]

where \(l_x \le l_y \le l_z\) are the three eigenvalues of the gyration
tensor. A general description of these parameters is provided in
(Mattice) while an application to polymer systems
can be found in (Theodorou). The asphericity is always
non-negative and zero only when the three principal moments are equal.
This zero condition is met when the distribution of particles is spherically
symmetric (hence the name asphericity) but also whenever the particle
distribution is symmetric with respect to the three coordinate axes (e.g.,
when the particles are distributed uniformly on a cube, tetrahedron, or other
Platonic solid). The acylindricity is always non-negative and zero only when
the two principal moments are equal. This zero condition is met when the
distribution of particles is cylindrically symmetric (hence the name,
acylindricity), but also whenever the particle distribution is symmetric with
respect to the two coordinate axes (e.g., when the particles are distributed
uniformly on a regular prism). The relative shape anisotropy
is bounded between 0 (if all points are spherically symmetric) and 1
(if all points lie on a line).

The tensor keyword must be specified in the compute gyration/chunk command.

Note
The coordinates of an atom contribute to the gyration tensor in
 unwrapped  form, by using the image flags associated with each atom.
See the dump custom command for a discussion of  unwrapped 
coordinates. See the Atoms section of the read_data
command for a discussion of image flags and how they are set for each
atom.  You can reset the image flags (e.g., to 0) before invoking this
compute by using the set image command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 molecule gyration/shape/chunk pe
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute gyration/chunk](compute_gyration_chunk.html)
- [compute gyration/shape](compute_gyration_shape.html)

