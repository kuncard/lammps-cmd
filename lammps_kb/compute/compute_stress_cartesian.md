---
id: compute_stress_cartesian
title: "compute stress/cartesian command"
url: https://docs.lammps.org/compute_stress_cartesian.html
---

# compute stress/cartesian command

## Syntax

```
compute ID group-ID stress/cartesian args
stress/cartesian args = dim1 bin_width1 dim2 bin_width2 keyword
  dim1 = x or y or z
  bin_width1 = width of the bin
  dim2 = x or y or z or NULL
  bin_width2 = width of the bin
  keyword = ke or pair or bond
```

## Description

Compute stress/cartesian defines computations that calculate profiles of the
diagonal components of the local stress tensor over one or two Cartesian
dimensions, as described in (Ikeshoji). The stress tensor is
split into a kinetic contribution \(P^k\) and a virial contribution
\(P^v\). The sum gives the total stress tensor \(P = P^k+P^v\).
This compute obeys momentum balance through fluid interfaces. They use the
Irving Kirkwood contour, which is the straight line between particle pairs.

Added in version 15Jun2023: Added support for bond styles

This compute only supports pair and bond (no angle, dihedral, improper,
or kspace) forces. By default, if no extra keywords are specified, all
supported contributions to the stress are included (ke, pair, bond). If any
keywords are specified, then only those components are summed.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all stress/cartesian x 0.1 NULL 0
compute 1 all stress/cartesian y 0.1 z 0.1
compute 1 all stress/cartesian x 0.1 NULL 0 ke pair
```

## Restrictions

Restrictions 
These computes calculate the stress tensor contributions for pair and bond
forces only (no angle, dihedral, improper, or kspace force).
It requires pairwise force calculations not available for most
many-body pair styles.
These computes are part of the EXTRA-COMPUTE package.  They are only
enabled if LAMMPS was built with that package.  See the Build
package doc page for more info.

## Related Commands

- [compute stress/atom](compute_stress_atom.html)
- [compute pressure](compute_pressure.html)
- [compute stress/mop/profile](compute_stress_mop.html)
- [compute stress/spherical](compute_stress_curvilinear.html)
- [compute stress/cylinder](compute_stress_curvilinear.html)

